from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from cleaning import clean_text
from sentiment_module import classify_sentiment
from extras import categorize_comment, detect_toxicity


def aggregate(comments_list, top_k_keywords=15):

    texts = [c['text'] for c in comments_list]

    # sentiment
    sentiments = [classify_sentiment(t) for t in texts]
    labels = [s['label'] for s in sentiments]
    counts = Counter(labels)
    total = len(texts)

    # comment categories
    categories = [categorize_comment(t) for t in texts]
    cat_counts = Counter(categories)

    # toxicity detection
    toxic_flags = [detect_toxicity(t) for t in texts]
    toxic_comments = [comments_list[i] for i, flag in enumerate(toxic_flags) if flag]

    # keywords using tfidf
    clean_texts = [clean_text(t) for t in texts]
    vect = TfidfVectorizer(max_features=2000, ngram_range=(1,2))
    X = vect.fit_transform(clean_texts)
    
    avg = np.asarray(X.mean(axis=0)).ravel()
    top_idx = np.argsort(avg)[-top_k_keywords:][::-1]
    keywords = [vect.get_feature_names_out()[i] for i in top_idx]

    # top comments by likes
    top_comments = sorted(comments_list, key=lambda x: x.get('likeCount',0), reverse=True)[:5]

    return {
        "sentiment_counts": counts,
        "sentiment_percent": {k: v/total for k,v in counts.items()},
        "category_counts": cat_counts,
        "toxic_comments": toxic_comments,
        "keywords": keywords,
        "top_comments": top_comments
    }
