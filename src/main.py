# src/main.py
from scraper.fetcher import fetch_all
import os

# List of target route URLs
route_ids = ["97", "8", "10"]
base_url = "https://www.bctransit.com/kelowna/schedules-and-maps/route-overview/?route="
urls = [base_url + route_id for route_id in route_ids]