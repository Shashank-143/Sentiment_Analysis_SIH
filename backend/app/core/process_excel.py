import asyncio
import pandas as pd
import os
import io
import base64
from datetime import datetime

from core.keyword_model import extract_keywords_async
from core.sentiment_model import analyze_sentiment
from core.summariser_model import generate_summary
from core.wordcloud_gen import create_wordcloud

OUTPUT_DIR = "outputs"

async def process_excel(input_file: str, output_file: str = None):
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"processed_results_{timestamp}.xlsx"

    df = pd.read_excel(input_file)

    if "comment_id" not in df.columns or "comment" not in df.columns:
        raise ValueError("Excel must contain 'comment_id' and 'comment' columns")

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

        # --- Run async NLP functions ---
        keywords = await extract_keywords_async(comment, top_n=5)
        sentiment_label, sentiment_score, confidence = await analyze_sentiment(comment)
        summary = await generate_summary(comment)

        # --- Generate wordcloud and encode as base64 ---
        wc_buffer = create_wordcloud(comment)
        wc_base64 = base64.b64encode(wc_buffer.getbuffer()).decode('utf-8')
        
        # --- Update the dataframe in place ---
        df.at[idx, "keywords"] = ", ".join(keywords) if keywords else ""
        df.at[idx, "sentiment"] = sentiment_label
        df.at[idx, "sentiment_score"] = sentiment_score
        df.at[idx, "confidence"] = confidence
        df.at[idx, "summary"] = summary
        df.at[idx, "wordcloud"] = wc_base64

    excel_output = io.BytesIO()
    with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    # If output_file is a path, save to disk
    if isinstance(output_file, str):
        with open(output_file, 'wb') as f:
            f.write(excel_output.getvalue())
        print(f"\n✅ Processing complete. Results saved to {output_file}")
        return output_file
    
    # Otherwise return the BytesIO object for download
    excel_output.seek(0)
    return excel_output


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
