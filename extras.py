TOXIC_WORDS = ["stupid", "idiot", "hate", "trash", "ugly", "nonsense"]

def categorize_comment(text):
    t = text.lower()
    
    if "?" in t or "how" in t or "why" in t:
        return "QUESTION"
    if "pls" in t or "can you" in t or "should" in t:
        return "SUGGESTION"
    if any(word in t for word in ["bad", "terrible", "worst", "awful"]):
        return "CRITICISM"
    if any(word in t for word in ["love", "great", "amazing", "awesome"]):
        return "APPRECIATION"
    
    return "NEUTRAL"


def detect_toxicity(text):
    t = text.lower()
    return any(word in t for word in TOXIC_WORDS)


def auto_reply(text, sentiment):
    if sentiment == "POSITIVE":
        return "Thank you! I'm glad you enjoyed it 😊"
    elif sentiment == "NEGATIVE":
        return "Thanks for your feedback, I'll try to improve!"
    elif sentiment == "NEUTRAL":
        return "Appreciate your comment 👍"
    elif sentiment == "QUESTION":
        return "Thanks for asking! I'll try to answer or cover this topic soon 😊"
    elif sentiment == "SUGGESTION":
        return "Nice suggestion! I'll keep it in mind 👌"
