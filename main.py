import json
from youtube_fetch import fetch_comments
from aggregator import aggregate
from extras import auto_reply
from sentiment_module import classify_sentiment

#Fetch comments
api = "AIzaSyCXGGghh2Tmgn_6ljFHevnJvlo-WVpxxZM"
video = "YQHsXMglC9A"

comments = fetch_comments(api, video, 60)

# Add test toxic comment BEFORE aggregation
comments.append({"text": "You are stupid and this is trash!", "likeCount": 0})

result = aggregate(comments)

#Output
print("\nSENTIMENT SUMMARY")
print(result["sentiment_counts"])
print(result["sentiment_percent"])

print("\nCOMMENT TYPE BREAKDOWN")
print(result["category_counts"])

print("\nTOXIC COMMENTS DETECTED")
for c in result["toxic_comments"]:
    print(f"- {c['text']} (Likes: {c['likeCount']})")

print("\nTOP KEYWORDS")
print(result["keywords"])

print("\nTOP COMMENTS")
for c in result["top_comments"]:
    print(f"- {c['text']} (Likes: {c['likeCount']})")

print("\nAUTO-REPLIES")
for c in comments:
    sentiment = classify_sentiment(c["text"])["label"]
    reply = auto_reply(c["text"], sentiment)
    print(f"Comment: {c['text']}")
    print(f"Reply → {reply}\n")
