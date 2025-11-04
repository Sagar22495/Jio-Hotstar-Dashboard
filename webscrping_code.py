import requests
import pandas as pd

# We'll use Hotstar's public API for catalog listings (unofficial but public)
url = "https://api.hotstar.com/o/v1/tray/find?client=web&count=20&offset=0&moreDetail=1&query=movies"

response = requests.get(url)
data = response.json()

# Extract items
items = data.get('body', {}).get('results', [])

dataset = []
for i, item in enumerate(items, start=1):
    dataset.append({
        "id": i,
        "type": "Movie" if "movie" in item.get("contentType", "").lower() else "Show",
        "title": item.get("title"),
        "director": item.get("director", "N/A"),
        "cast": ", ".join(item.get("actors", [])) if item.get("actors") else "N/A",
        "release_year": item.get("year", "N/A"),
        "rating": item.get("rating", "N/A"),
        "duration": item.get("duration", "N/A"),
    })

# Convert to DataFrame
df = pd.DataFrame(dataset)

# Save to CSV
df.to_csv("hotstar_dataset.csv", index=False)
print("✅ Dataset saved as hotstar_dataset.csv")
