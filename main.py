import json
from youtube_fetch import fetch_comments
from aggregator import aggregate

# ---- Fetch comments ----
api = "AIzaSyCXGGghh2Tmgn_6ljFHevnJvlo-WVpxxZM"
video = "YQHsXMglC9A"   # extracted ID

comments = fetch_comments(api, video, 60)

result = aggregate(comments)

# ---- Output ----
print("\nSENTIMENT SUMMARY")
print(result["sentiment_counts"])
print(result["sentiment_percent"])

print("\nCOMMENT TYPE BREAKDOWN")
print(result["category_counts"])

comments.append({"text": "You are stupid and this is trash!", "likeCount": 0}) # test toxic comment
print("\nTOXIC COMMENTS DETECTED")
for c in result["toxic_comments"]:
    print(f"- {c['text']} (Likes: {c['likeCount']})")

print("\nTOP KEYWORDS")
print(result["keywords"])

print("\nTOP COMMENTS")
for c in result["top_comments"]:
    print(f"- {c['text']} (Likes: {c['likeCount']})")
