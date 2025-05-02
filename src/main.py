# src/main.py
from scraper.fetcher import fetch_all
from scraper.parser import parse_schedule_html
import pandas as pd
import os
import glob

def main():
    # === 1. Define route URLs ===
    route_ids = ["97", "8", "10"]
    base_url = "https://www.bctransit.com/kelowna/schedules-and-maps/route-overview/?route="
    urls = [base_url + route_id for route_id in route_ids]

    # === 2. Fetch all pages using multithreading ===
    print("Fetching route pages...")
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

    # === 3. Parse all saved HTML files ===
    print("\n Parsing saved HTML files...")
    raw_files = glob.glob("data/raw/*.html")
    os.makedirs("data/processed", exist_ok=True)

    for file_path in raw_files:
        route_id = os.path.basename(file_path).split('_')[-1].replace('.html', '')
        trips = parse_schedule_html(file_path)

        if trips:
            df = pd.DataFrame(trips)
            output_path = f"data/processed/route_{route_id}.csv"
            df.to_csv(output_path, index=False)
            print(f"Parsed and saved {len(trips)} trips → {output_path}")
        else:
            print(f"No trips found in {file_path}")

    print("\n✅ All routes scraped, parsed, and saved.")

if __name__ == "__main__":
    main()
