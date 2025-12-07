# youtube_fetch.py
# STEP 2 — Fetch YouTube Comments Programmatically (mid-eval ready)

from googleapiclient.discovery import build
import re


def get_video_id(url_or_id):
    """
    Extracts a valid 11-char YouTube ID from:
    - raw ID
    - https://www.youtube.com/watch?v=ID&...
    - https://youtu.be/ID
    """
    match = re.search(r"(?:v=|youtu\.be/)([-_A-Za-z0-9]{11})", url_or_id)
    return match.group(1) if match else url_or_id


def fetch_comments(api_key, video_id, max_comments=300):
    """
    Fetches up to `max_comments` from YouTube CommentThreads API.
    Returns: list of dictionaries → each containing:
      - text
      - likeCount
      - author
      - publishedAt
    """

    # AUTHENTICATION to Google API
    youtube = build("youtube", "v3", developerKey=api_key)

    comments = []  # final list

    # first request — up to 100 comments per API call
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100
    )

    while request and len(comments) < max_comments:
        response = request.execute()  # send actual request → JSON response

        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({
                "text": snippet.get("textDisplay", ""),
                "likeCount": snippet.get("likeCount", 0),
                "author": snippet.get("authorDisplayName", ""),
                "publishedAt": snippet.get("publishedAt", "")
            })

            # (Optional) You could fetch replies here later

        # pagination: request next page
        request = youtube.commentThreads().list_next(request, response)

    return comments[:max_comments]


# 🔽 Testing / Running Section (only runs when executing script directly)
if __name__ == "__main__":
    # ❗ replace with YOUR NEW regenerated API key
    YOUTUBE_API_KEY = "AIzaSyCXGGghh2Tmgn_6ljFHevnJvlo-WVpxxZM"

    url = "https://www.youtube.com/watch?v=YQHsXMglC9A&list=RDYQHsXMglC9A&start_radio=1"

    video_id = get_video_id(url)
    print(f"Extracted Video ID: {video_id}")

    print("\nFetching comments...")

    data = fetch_comments(YOUTUBE_API_KEY, video_id, max_comments=200)

    print(f"Fetched {len(data)} comments.\n")

    # Print first 5 samples to verify
    for i, c in enumerate(data[:5]):
        print(f"Comment {i+1}:")
        print(" Author:", c["author"])
        print(" Likes :", c["likeCount"])
        print(" Text  :", c["text"])
        print(" Time  :", c["publishedAt"])
        print("-" * 50)

