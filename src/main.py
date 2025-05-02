# src/main.py
from scraper.fetcher import fetch_all
import os

# List of target route URLs
route_ids = ["97", "8", "10"]
base_url = "https://www.bctransit.com/kelowna/schedules-and-maps/route-overview/?route="
urls = [base_url + route_id for route_id in route_ids]

# Fetch HTML pages from relevant routes
html_pages = fetch_all(urls)

# Save raw HTML to /data/raw/
os.makedirs("data/raw", exist_ok=True)

# Saves all the scraped HTML pages into cleanly named files in data/raw/
for url, html in html_pages.items():
    route_id = url.split("=")[-1]
    file_path = f"data/raw/route_{route_id}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
        print(f"[✔] Saved HTML for route {route_id} → {file_path}")