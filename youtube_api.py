import random
from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build

YOUTUBE_API_KEY = "AIzaSyC7EAM1C0mlUKIeBujo9PnEmn6QbJw-XUg"

def search_youtube_music(query, max_results=10):
    """Search YouTube for music videos using youtubesearchpython."""
    try:
        videos_search = VideosSearch(query, limit=max_results)
        results = []
        unique_video_ids = set()  # Ensure uniqueness

        for result in videos_search.result().get("result", []):
            video_id = result.get("id", {}).get("videoId")
            if video_id and video_id not in unique_video_ids:
                video_info = {
                    "title": result.get("title", "No Title"),
                    "url": result.get("link", "#"),
                    "thumbnail": result.get("thumbnails", [{}])[0].get("url", ""),
                }
                results.append(video_info)
                unique_video_ids.add(video_id)

        random.shuffle(results)  # Shuffle after filtering duplicates
        return results[:max_results]  # Trim down if necessary

    except Exception as e:
        print(f"[search_youtube_music] Error: {e}")
        return []

def get_youtube_videos(query, max_results=10):
    """Fetch YouTube videos using API, with fallback if quota exceeds."""
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            part="snippet",
            maxResults=max_results,
            q=query,
            type="video"
        )
        response = request.execute()
        
        results = []
        unique_video_ids = set()  # Prevent duplicates

        for item in response.get("items", []):
            video_id = item["id"].get("videoId")
            if video_id and video_id not in unique_video_ids:
                title = item["snippet"].get("title", "No Title")
                thumbnail = item["snippet"]["thumbnails"]["medium"].get("url", "")
                url = f"https://www.youtube.com/watch?v={video_id}"
                results.append({
                    "title": title,
                    "url": url,
                    "thumbnail": thumbnail,
                })
                unique_video_ids.add(video_id)

        random.shuffle(results)  # Improve diversity in results
        return results[:max_results]  # Trim final list

    except Exception as e:
        if "quotaExceeded" in str(e):
            print("[get_youtube_videos] Quota exceeded. Using fallback.")
            return search_youtube_music(query, max_results)
        else:
            print(f"[get_youtube_videos] Error: {e}")
            return []
