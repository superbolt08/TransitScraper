import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"[✓] Fetched: {url}")
        return url, response.text
    except Exception as e:
        print(f"[X] Failed: {url} | Reason: {e}")
        return url, None

# Function to fetch many pages in parallel using multithreading
def fetch_all(urls, max_workers = 4):
    # Create a thread pool with up to max_workers threads
    results = {}

    # Submit fetch_page(url) to the thread pool for each URL
    # This creates a "future" object for each task, which runs in the background
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetch_page, url): url for url in urls}

        # Wait for the futures to complete, in the order they finish (fastest first)
        for future in as_completed(future_to_url):
            url, html = future.result()
        
            if html:  # Only store the result if the HTML was successfully fetched
                results[url] = html  # Add to the results dictionary
                time.sleep(0.5)  # Pause briefly to avoid hitting the site too fast
                
    return results # Return all fetched HTML content as a dictionary