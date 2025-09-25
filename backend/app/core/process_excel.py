import asyncio
import pandas as pd
import openpyxl
from openpyxl.drawing.image import Image as XlImage
import os
import io
import base64
import tempfile
import time
from datetime import datetime
from PIL import Image as PILImage

from core.keyword_model import extract_keywords_async
from core.sentiment_model import analyze_sentiment
from core.summariser_model import generate_summary
from core.wordcloud_gen import create_wordcloud

OUTPUT_DIR = "outputs"

async def process_excel(input_file: str, output_file: str = None):
    # Generate a unique process ID for tracking
    process_id = f"excel_{int(time.time())}_{os.getpid()}"
    temp_files = []  # Track temp files for cleanup
    
    try:
        print(f"[{process_id}] Starting Excel processing")
        if not os.path.exists(input_file):
            raise ValueError(f"Input file does not exist: {input_file}")
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"processed_results_{timestamp}.xlsx"
        
        try:
            df = pd.read_excel(input_file)
            print(f"Columns found in Excel: {list(df.columns)}")
        except Exception as e:
            raise ValueError(f"Failed to read Excel file: {str(e)}")
        
        df.columns = [col.lower() for col in df.columns]
        
        required_columns = ["comment_id", "comment"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            available_cols = [col.lower() for col in df.columns]
            similar_cols = {
                "comment_id": [c for c in available_cols if "id" in c or "comment" in c],
                "comment": [c for c in available_cols if "comment" in c or "text" in c or "feedback" in c]
            }
            
            error_msg = f"Excel file is missing required columns: {', '.join(missing_columns)}. "
            for missing in missing_columns:
                if similar_cols[missing]:
                    error_msg += f"\nFound similar columns for '{missing}': {', '.join(similar_cols[missing])}"
            
            error_msg += "\n\nPlease ensure your Excel file has the columns 'comment_id' and 'comment'."
            raise ValueError(error_msg)
            
        # Initialize columns
        if "keywords" not in df.columns:
            df["keywords"] = ""
        if "sentiment" not in df.columns:
            df["sentiment"] = ""
        if "sentiment_score" not in df.columns:
            df["sentiment_score"] = None
        if "confidence" not in df.columns:
            df["confidence"] = None
        if "summary" not in df.columns:
            df["summary"] = ""
        if "wordcloud" not in df.columns:
            df["wordcloud"] = ""

        for idx, row in df.iterrows():
            comment_id = row["comment_id"]
            comment = str(row["comment"]).strip()

            if not comment:
                continue

            print(f"Processing Comment ID {comment_id}...")

            try:
                # --- Run async NLP functions ---
                keywords = await extract_keywords_async(comment, top_n=5)
                sentiment_label, sentiment_score, confidence = await analyze_sentiment(comment)
                summary = await generate_summary(comment)

                wc_buffer = create_wordcloud(comment)
                wc_base64 = base64.b64encode(wc_buffer.getbuffer()).decode('utf-8')
                
                df.at[idx, "keywords"] = ", ".join(keywords) if keywords else ""
                df.at[idx, "sentiment"] = sentiment_label
                df.at[idx, "sentiment_score"] = sentiment_score
                df.at[idx, "confidence"] = confidence
                df.at[idx, "summary"] = summary
                df.at[idx, "wordcloud"] = wc_base64  # Store base64 data for now
            except Exception as e:
                print(f"Error processing comment ID {comment_id}: {str(e)}")
                df.at[idx, "keywords"] = "Error processing"
                df.at[idx, "sentiment"] = "Error"
                df.at[idx, "sentiment_score"] = 0.0
                df.at[idx, "confidence"] = 0.0
                df.at[idx, "summary"] = f"Error: {str(e)}"
                df.at[idx, "wordcloud"] = ""

        # Create output file with images
        excel_output = io.BytesIO()
        temp_files = []  # Keep track of all temp files for cleanup
        
        try:
            print("Creating Excel output with images...")
            with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
                # First write the data without wordcloud column
                wordcloud_col = None
                if 'wordcloud' in df.columns:
                    wordcloud_col = df['wordcloud'].copy()
                    df['wordcloud'] = ""  # Clear it temporarily
                
                df.to_excel(writer, index=False)
                
                # Get the workbook and worksheet to add images
                if wordcloud_col is not None:
                    # Finish the pandas Excel writing process to get access to the workbook
                    writer.close()
                    
                    # Now open with openpyxl to add images
                    workbook = openpyxl.load_workbook(excel_output)
                    worksheet = workbook.active
                    
                    # Find the wordcloud column index
                    wordcloud_col_idx = list(df.columns).index('wordcloud') + 1  # +1 because Excel is 1-indexed
                    
                    # Add images to cells
                    for row_idx, wc_data in enumerate(wordcloud_col, start=2):  # Start from row 2 (skip header)
                        if wc_data and len(wc_data) > 100:  # Check if there's actual image data
                            try:
                                # Create a unique temp file name in a system temp directory
                                temp_dir = tempfile.gettempdir()
                                temp_img_path = os.path.join(temp_dir, f"wc_temp_{row_idx}_{os.getpid()}.png")
                                temp_files.append(temp_img_path)  # Track for later cleanup
                                
                                # Write the image data to the file
                                with open(temp_img_path, 'wb') as img_file:
                                    img_file.write(base64.b64decode(wc_data))
                                
                                # Verify the file was created
                                if not os.path.exists(temp_img_path):
                                    raise FileNotFoundError(f"Failed to create temp image file at {temp_img_path}")
                                
                                # Add image to the cell
                                img = XlImage(temp_img_path)
                                # Scale down the image to fit in an Excel cell
                                img.width = 250
                                img.height = 120
                                cell = worksheet.cell(row=row_idx, column=wordcloud_col_idx)
                                worksheet.add_image(img, f"{cell.coordinate}")
                                
                            except Exception as img_err:
                                print(f"Could not add image for row {row_idx}: {str(img_err)}")
                    
                    try:
                        # Save the workbook to the BytesIO object
                        print(f"[{process_id}] Saving workbook with {len(temp_files)} images...")
                        excel_output.seek(0)
                        excel_output.truncate(0)
                        workbook.save(excel_output)
                        print(f"[{process_id}] Workbook saved successfully")
                    finally:
                        # Clean up temp files after Excel is saved
                        print("Cleaning up temporary image files...")
                        for temp_path in temp_files:
                            try:
                                if os.path.exists(temp_path):
                                    os.unlink(temp_path)
                            except Exception as cleanup_err:
                                print(f"Warning: Could not remove temp file {temp_path}: {str(cleanup_err)}")
        except Exception as e:
            raise ValueError(f"Failed to write Excel file: {str(e)}")
        
        # If output_file is a path, save to disk
        if isinstance(output_file, str):
            try:
                with open(output_file, 'wb') as f:
                    f.write(excel_output.getvalue())
                print(f"\n✅ Processing complete. Results saved to {output_file}")
                # Always return BytesIO object regardless of whether we saved to disk
            except Exception as e:
                raise ValueError(f"Failed to save output file: {str(e)}")
        
        # Return the BytesIO object for download
        excel_output.seek(0)
        return excel_output
        
    except Exception as e:
        import traceback
        print(f"[{process_id}] Error in process_excel: {str(e)}\n{traceback.format_exc()}")
        
        # Clean up any remaining temporary files
        for temp_path in temp_files:
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    print(f"[{process_id}] Cleaned up temp file: {temp_path}")
            except Exception as cleanup_err:
                print(f"[{process_id}] Failed to clean up temp file {temp_path}: {str(cleanup_err)}")
                
        # For production environments, ensure the error message is production-friendly
        if isinstance(e, ValueError):
            # Pass through ValueError messages as they're usually user-friendly
            raise
        else:
            # Sanitize internal errors for production
            raise ValueError(f"Excel processing failed: {type(e).__name__}. Please try again or contact support if the issue persists.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python process_excel.py <input_excel_file> [output_excel_file]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        result = asyncio.run(process_excel(input_file, output_file))
        if isinstance(result, io.BytesIO):
            print(f"\n✅ Processing complete. Excel file prepared for download.")
