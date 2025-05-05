# Transit Scraper

## Overview
The **Transit Scraper** is a Python-based project designed to scrape transit schedule data from a public transit website, process the data, and save it in a structured format (CSV). This tool is useful for analyzing transit schedules, visualizing route data, or integrating the data into other applications.

---

## Features
- **Scraping**: Fetches HTML pages for specified transit routes.
- **Parsing**: Extracts trip data (e.g., stop names, times) from the HTML files.
- **Data Processing**: Saves parsed data into CSV files for easy analysis.
- **Automation**: Handles multiple routes and organizes data into structured directories.

---

## Project Structure
```
TransitScraper/
│
├── data/
│   ├── raw/          # Raw HTML files saved after scraping
│   ├── processed/    # Processed CSV files with parsed trip data
│
├── src/
│   ├── main.py       # Main script to run the scraper
│   ├── scraper/
│       ├── fetcher.py    # Handles fetching HTML pages
│       ├── parser.py     # Parses HTML files to extract trip data
│
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## Requirements
- Python 3.8 or higher
- Libraries:
  - `pandas`
  - `requests`
  - `beautifulsoup4`

Install dependencies using:
```bash
pip install -r [requirements.txt](http://_vscodecontentref_/4)
```

## Usage
### Define Routes

- Update the route_ids list in src/main.py with the desired route IDs.

### Run the Scraper
- Execute the main script:
```
python src/main.py
```
### Output

- Raw HTML files are saved in data/raw/.
- Parsed trip data is saved as CSV files in data/processed/.


## Example
For the following routes:
- Route 97
- Route 8
- Route 10

The scraper will:
1. Fetch HTML pages from:
   ```
   https://www.bctransit.com/kelowna/schedules-and-maps/route-overview/?route=97
   https://www.bctransit.com/kelowna/schedules-and-maps/route-overview/?route=8
   https://www.bctransit.com/kelowna/schedules-and-maps/route-overview/?route=10
   ```
2. Save the HTML files in `data/raw/` as:
   ```
   data/raw/route_97.html
   data/raw/route_8.html
   data/raw/route_10.html
   ```
3. Parse the HTML files and save the trip data as:
   ```
   data/processed/route_97.csv
   data/processed/route_8.csv
   data/processed/route_10.csv
   ```

---
## 🧪 Command-Line Interface (CLI)

The project includes a CLI powered by `argparse`, allowing you to run specific parts of the pipeline directly from the command line.

### 📌 Basic Format

```
python src/main.py --mode <fetch|parse|visualize> [--route ROUTE_ID]
```

#### Arguments:
1. **`--mode`** (required):
   - Specifies the action to perform.
   - Options:
     - `fetch`: Scrape transit schedule data and save raw HTML files.
     - `parse`: Process the saved HTML files and generate CSV files with trip data.
     - `visualize`: Visualize trip data for a specific route.
     - `all`: Does all of the above with the default path for route 97

2. **`--route`** (optional, required for `visualize` mode):
   - Specifies the route number to visualize.
   - Example: `--route 97`

#### 1. Fetch Transit Data
To scrape transit schedule data for all defined routes:
```bash
python src/main.py --mode fetch
```
This will save raw HTML files in the `data/raw/` directory.

#### 2. Parse Transit Data
To process the saved HTML files and generate CSV files:
```bash
python src/main.py --mode parse
```
This will save processed CSV files in the `data/processed/` directory.

#### 3. Visualize Transit Data
To visualize trip data for a specific route (e.g., route 97):
```bash
python src/main.py --mode visualize --route 97
```
This will display a graph or chart (depending on your `plot_trip_frequency` implementation).

#### 4. Run all commands
Runs the full pipeline: fetches HTML, parses data into CSV, and visualizes the specified route.

`--mode all [--route <ROUTE_ID>]`
```bash
python src/main.py --mode all --route 97
```
---
### 🛑 Error Handling
- If you run `--mode visualize` without specifying a route:
  ```bash
  python src/main.py --mode visualize
  ```
  The script will display:
  ```
  [❌] You must specify --route when using --mode visualize. Example: --route 97
  ```

- If the CSV file for the specified route does not exist:
  ```
  [❌] CSV not found: data/processed/route_<ROUTE_ID>.csv. Ensure you have run the script with --mode parse first.
  ```

## Customization
- **Add More Routes**:
  - Modify the `route_ids` list in `src/main.py` to include additional route IDs.
- **Change Output Format**:
  - Update the `main.py` script to save data in other formats (e.g., JSON).

---

## Future Improvements
- Add error handling for failed fetches or parsing errors.
- Implement logging instead of print statements.
- Use multithreading for faster parsing of large datasets.
- Add unit tests for `fetcher.py` and `parser.py`.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments
- **BeautifulSoup**: For HTML parsing.
- **Pandas**: For data processing and CSV generation.
- **BC Transit**: For providing publicly accessible transit schedule data.