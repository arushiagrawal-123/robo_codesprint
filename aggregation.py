from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def aggregate(comments_list, sentiment_func, top_k_keywords=15):
    # comments_list: list of dicts {'text':..., 'likeCount':...}
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
