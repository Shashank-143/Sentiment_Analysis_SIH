import asyncio
import pandas as pd
import os

from keyword_model import extract_keywords_async
from sentiment_model import analyze_sentiment
from summariser_model import generate_summary
from wordcloud_gen import create_wordcloud

OUTPUT_DIR = "outputs"

async def process_excel(input_file: str, output_file: str = "processed_results.xlsx"):
    """Process Excel file with comments using NLP pipeline."""

    # 1. Read Excel file
    df = pd.read_excel(input_file)

    if "comment_id" not in df.columns or "comment" not in df.columns:
        raise ValueError("Excel must contain 'comment_id' and 'comment' columns")

    results = []

    # 2. Loop over each row
    for _, row in df.iterrows():
        comment_id = row["comment_id"]
        comment = str(row["comment"]).strip()

        if not comment:
            continue

        print(f"Processing Comment ID {comment_id}...")

        # --- Run async NLP functions ---
        keywords = await extract_keywords_async(comment, top_n=5)
        sentiment_label, sentiment_score, confidence = await analyze_sentiment(comment)
        summary = await generate_summary(comment)

        # --- Wordcloud (save per comment) ---
        """os.makedirs(OUTPUT_DIR, exist_ok=True)
        wc_buffer = create_wordcloud(comment)
        wc_path = os.path.join(OUTPUT_DIR, f"wordcloud_{comment_id}.png")
        with open(wc_path, "wb") as f:
            f.write(wc_buffer.getbuffer())"""

        # Collect results
        results.append({
            "comment_id": comment_id,
            "comment": comment,
            "keywords": ", ".join(keywords) if keywords else "",
            "sentiment": sentiment_label,
            "sentiment_score": sentiment_score,
            "confidence": confidence,
            "summary": summary
            #"wordcloud_path": wc_path
        })

    # 3. Save results to new Excel
    result_df = pd.DataFrame(results)
    result_df.to_excel(output_file, index=False)
    print(f"\n✅ Processing complete. Results saved to {output_file}")
    #print(f"✅ Wordclouds saved in {OUTPUT_DIR}/")

# 4. Run as script
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python process_excel.py <input_excel_file>")
    else:
        asyncio.run(process_excel(sys.argv[1]))
