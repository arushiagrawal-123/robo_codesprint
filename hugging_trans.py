from transformers import pipeline
sentiment_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify_sentiment(text):
    out = sentiment_pipe(text[:512])  # limit to 512 tokens
    return out[0]   # e.g. {'label': 'POSITIVE', 'score': 0.999}
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_comments(texts, max_chunk=1000):
    # naive: join many comments into one doc, chunk if too long
    doc = " ".join(texts)
    if len(doc) < 800:
        s = summarizer(doc, max_length=80, min_length=30, do_sample=False)
        return s[0]['summary_text']
    # chunking
    chunks = [doc[i:i+800] for i in range(0, len(doc), 800)]
    summaries = [summarizer(c, max_length=60, min_length=20, do_sample=False)[0]['summary_text'] for c in chunks]
    return " ".join(summaries)
zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_topic(text, candidate_labels):
    res = zero_shot(text, candidate_labels)
    return res  # labels & scores
