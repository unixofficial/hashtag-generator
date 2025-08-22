import json
import requests

def handler(request, response):
    # Get query parameters
    keywords = request.args.get("keywords", "").strip() or request.args.get("k", "").strip()

    # If no keywords provided
    if not keywords:
        return response.json({
            "success": False,
            "error": "Missing keywords parameter. Use ?keywords= or ?k= in the query string."
        }, status=400)

    url = "https://www.veed.io/script-generator-ap/api/generate-non-streaming-text"
    payload = {
        "topic": None,
        "keywords": keywords,
        "vibe": None,
        "format": None,
        "slug": "hashtag-generator",
        "number": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "origin": "https://www.veed.io",
        "referer": "https://www.veed.io/tools/script-generator/hashtag-generator",
    }

    try:
        res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        res.raise_for_status()
    except requests.RequestException as e:
        return response.json({
            "success": False,
            "error": str(e)
        }, status=500)

    try:
        hashtags_raw = res.json()
    except ValueError:
        return response.json({
            "success": False,
            "error": "Invalid JSON response from API"
        }, status=502)

    hashtags = []
    if isinstance(hashtags_raw, list) and len(hashtags_raw) == 1 and isinstance(hashtags_raw[0], str):
        hashtags = hashtags_raw[0].strip().split()
    elif isinstance(hashtags_raw, list):
        hashtags = hashtags_raw
    else:
        hashtags = [hashtags_raw]

    return response.json({
        "success": True,
        "keywords": keywords,
        "hashtags": hashtags
    })
