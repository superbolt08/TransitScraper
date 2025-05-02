# src/main.py
from scraper.fetcher import fetch_all
from scraper.parser import parse_schedule_html
import os
import glob

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

# Parse the saved HTML files
raw_files = glob.glob("data/raw/*.html")
for file_path in raw_files:
    trips = parse_schedule_html(file_path)
    print(f"[✔] Parsed {file_path}: {len(trips)} trips found")