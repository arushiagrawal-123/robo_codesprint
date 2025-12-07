# sentiment_module.py

# A single entrypoint for sentiment classification used by aggregator.py:
# classify_sentiment(text) -> {"label": "POSITIVE"/"NEGATIVE"/"NEUTRAL", "score": float}

try:
    # optional: huggingface pipeline if available
    from transformers import pipeline
    _hf_available = True
except Exception:
    _hf_available = False

# simple rule-based fallback
def dummy_sentiment(text):
    t = text.lower()
    if any(w in t for w in ["love", "great", "amazing", "wow", "awesome"]):
        return {"label": "POSITIVE", "score": 0.95}
    if any(w in t for w in ["bad", "hate", "worst", "terrible", "awful"]):
        return {"label": "NEGATIVE", "score": 0.90}
    return {"label": "NEUTRAL", "score": 0.60}

# if transformers available, prepare pipeline lazily
_hf_pipe = None
def _init_hf():
    global _hf_pipe
    if _hf_pipe is None:
        _hf_pipe = pipeline("sentiment-analysis", truncation=True)

def classify_sentiment(text):
    """
    Unified sentiment API for the project.
    Tries HuggingFace if present, otherwise uses dummy rules.
    Returns: dict { "label": str, "score": float }
    """
    if not text or not isinstance(text, str):
        return {"label": "NEUTRAL", "score": 0.0}

    if _hf_available:
        try:
            _init_hf()
            out = _hf_pipe(text[:512])  # keep input short for HF
            # HF returns list of one dict
            return {"label": out[0]["label"], "score": float(out[0]["score"])}
        except Exception:
            # degrade gracefully to dummy if HF fails
            return dummy_sentiment(text)
    else:
        return dummy_sentiment(text)
