from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

def create_wordcloud(sentence: str) -> BytesIO:
    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="rainbow",
        prefer_horizontal=1.0,
        collocations=False
    ).generate(sentence)

    buffer = BytesIO()
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    return buffer