import requests
import time

def test_semantic_scholar(paper_title):
    title = " ".join(paper_title.replace("\n", " ").split())
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "limit": 1,
        "fields": "title,citationCount,influentialCitationCount,venue"
    }
    headers = {
        "User-Agent": "LongevityBot/1.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        print("🔧 Status:", response.status_code)
        print("📨 Raw response:", response.text)

        if response.status_code == 200:
            data = response.json()
            if data["data"]:
                paper = data["data"][0]
                print("✅ Found paper:", paper["title"])
                print("📊 Citations:", paper.get("citationCount"))
                print("🏛 Venue:", paper.get("venue"))

        else:
            print("❌ Error: ", response.status_code)

    except Exception as e:
        print("⚠️ Exception:", e)

    time.sleep(1)
