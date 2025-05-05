# src/main.py
from scraper.fetcher import fetch_all
from scraper.parser import parse_schedule_html
from visualizer import plot_trip_frequency
import pandas as pd
import os
import glob
import argparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # show in terminal
        logging.FileHandler("logs/run.log", mode='a', encoding='utf-8')  # save to file
    ]
)


def fetch_routes():
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

def parse_files():
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


def main():
    parser = argparse.ArgumentParser(description="Transit Scraper CLI")
    parser.add_argument("--mode", type=str, required=True,
                        choices=["fetch", "parse", "visualize", "all"],
                        help="What action to perform")

    parser.add_argument("--route", type=str,
                        help="Route number to visualize (used with mode=visualize)")

    args = parser.parse_args()

    if args.mode == "fetch":
        fetch_routes()
    elif args.mode == "parse":
        parse_files()
    elif args.mode == "visualize":  # === 4. Vizualize route ===
        if not args.route:
            print("[❌] You must specify --route when using --mode visualize")
        else:
            path = f"data/processed/route_{args.route}.csv"
            if os.path.exists(path):
                plot_trip_frequency(path)
            else:
                print(f"[❌] CSV not found: {path}")
    elif args.mode == "all":
        fetch_routes()
        parse_files()

        default_route = args.route if args.route else "97"
        path = f"data/processed/route_{default_route}.csv"

        if os.path.exists(path):
            plot_trip_frequency(path)
        else:
            print(f"[❌] CSV not found for route {default_route}")
                
if __name__ == "__main__":
    main()
