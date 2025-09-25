from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

def create_wordcloud(sentence: str) -> BytesIO:
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="viridis",  # A color map with better contrast
        prefer_horizontal=0.9,  # Allow some vertical words for better packing
        collocations=False,
        min_font_size=10,  # Ensure text is readable
        max_font_size=150,  # Allow for prominent keywords
        random_state=42  # For reproducible results
    ).generate(sentence)

    buffer = BytesIO()
    plt.figure(figsize=(10, 6), dpi=150)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(buffer, format="png", bbox_inches='tight', 
                dpi=150, transparent=False, 
                facecolor='white', edgecolor='none')
    plt.close()
    buffer.seek(0)

    return buffer