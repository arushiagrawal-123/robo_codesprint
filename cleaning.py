import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Auto-download tokenizer on first run
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Might also need punkt_tab for new nltk versions
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

stop_words = set(stopwords.words("english"))


def clean_text(text, remove_stopwords=True):
    """
    Lowercase, remove URLs, punctuation, and optionally stopwords.
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    if remove_stopwords:
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in stop_words]
        text = " ".join(tokens)

    return text
