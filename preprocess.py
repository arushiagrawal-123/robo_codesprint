import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))
def clean_text(text, remove_stopwords=True):
    """
    Cleans the input text by:
    - Lowercasing
    - Removing URLs
    - Removing special characters
    - Optionally removing stopwords
    """
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    if remove_stopwords:
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in stop_words]
        text = ' '.join(filtered_tokens)

    return text
from transformers import pipeline
sentiment_pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify_sentiment(text):
    out = sentiment_pipe(text[:512])  
    return out[0]   # {'label': 'POSITIVE', 'score': 0.999}
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_comments(texts, max_chunk=1000):
    # join many comments into one doc, chunk if too long
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
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def aggregate(comments_list, sentiment_func, top_k_keywords=15):
   
    texts = [c['text'] for c in comments_list]
    # sentiment
    sentiments = [sentiment_func(t) for t in texts]  # label+score
    labels = [s['label'] for s in sentiments]
    counts = Counter(labels)
    total = len(texts)

    # keywords using TF-IDF
    clean_texts = [clean_text(t) for t in texts]
    vect = TfidfVectorizer(max_features=2000, ngram_range=(1,2))
    X = vect.fit_transform(clean_texts)
    # average tfidf weights to pick top features across corpus
    avg = np.asarray(X.mean(axis=0)).ravel()
    top_idx = np.argsort(avg)[-top_k_keywords:][::-1]
    keywords = [vect.get_feature_names_out()[i] for i in top_idx]

    # top comments by likes:
    top_comments = sorted(comments_list, key=lambda x: x.get('likeCount',0), reverse=True)[:5]

    return {
        'sentiment_counts': counts,
        'sentiment_percent': {k: v/total for k,v in counts.items()},
        'keywords': keywords,
        'top_comments': top_comments,
    }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
from youtube_fetch import fetch_comments

comments = fetch_comments("AIzaSyCXGGghh2Tmgn_6ljFHevnJvlo-WVpxxZM", "YQHsXMglC9A" , max_comments=200)
result = aggregate(comments, classify_sentiment)






print("\nSentiment Counts:", result["sentiment_counts"])
print("Sentiment Percentage:", result["sentiment_percent"])
print("Top Keywords:", result["keywords"])

print("\nTop Comments Based on Likes:")
for c in result["top_comments"]:
    print(f" {c['text']}  (Likes: {c['likeCount']})")
