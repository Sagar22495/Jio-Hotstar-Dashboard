import requests
import pandas as pd
import time

# Base API URL (Movies Category)
BASE_URL = "https://api.hotstar.com/o/v1/tray/gettray"
CATEGORY_ID = 3782   # Hotstar Movies Category ID
SIZE = 20            # Number of movies per request

all_movies = []
offset = 0

print("🔍 Fetching Hotstar movies...")

while True:
    params = {
        "offset": offset,
        "size": SIZE,
        "caller": "web",
        "categoryId": CATEGORY_ID
    }

    res = requests.get(BASE_URL, params=params)
    if res.status_code != 200:
        print("⚠️ Error fetching data, stopping.")
        break

    data = res.json()
    items = data.get("body", {}).get("results", [])
    if not items:
        print("✅ No more movies found. Stopping loop.")
        break

    # Extract movie details
    for item in items:
        movie = {
            "title": item.get("title"),
            "language": item.get("metaData", {}).get("language"),
            "genre": item.get("metaData", {}).get("genre"),
            "releaseYear": item.get("metaData", {}).get("releaseYear"),
            "duration": item.get("duration"),
            "url": "https://www.hotstar.com" + item.get("url", "")
        }
        all_movies.append(movie)

    print(f"✅ Fetched {len(items)} movies (Total: {len(all_movies)})")

    offset += SIZE
    time.sleep(1)  # avoid hitting API too fast

# Save to CSV
df = pd.DataFrame(all_movies)
df.drop_duplicates(subset=["url"], inplace=True)
df.to_csv("hotstar_movies_dataset.csv", index=False, encoding="utf-8")

print(f"\n🎬 Total Movies Saved: {len(df)}")
print("💾 File saved as hotstar_movies_dataset.csv")



