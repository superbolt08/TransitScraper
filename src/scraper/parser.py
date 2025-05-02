# src/scraper/parser.py
from bs4 import BeautifulSoup

def parse_schedule_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Get stop names from the table header
    table = soup.find('table')  # the main schedule table
    header = table.find('thead')
    stop_names = [th.get_text(strip=True) for th in header.find_all('th') if th.get_text(strip=True)]

    # Get all rows of times from the table body
    body = table.find('tbody')
    trips = []

    for row in body.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) < len(stop_names):
            continue  # skip if row is empty or has fewer times than stops

        # Skip the first cell if it's a note field (like `class="js-schedule-row-note"`)
        time_cells = cells[1:] if len(cells) == len(stop_names) + 1 else cells

        trip_times = [td.get_text(strip=True) for td in time_cells]
        trips.append(dict(zip(stop_names, trip_times)))

    return trips
