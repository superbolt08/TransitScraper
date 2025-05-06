from scraper.parser import parse_schedule_html
from bs4 import BeautifulSoup
import tempfile



def run_parser_on_html(html_str):
    import tempfile
    # Create a temporary file to simulate an HTML file for testing
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.html', delete=False) as f:
        f.write(html_str) # Write the sample HTML content into the temporary file
        f.seek(0) # Reset the file pointer to the beginning of the file so it can be read
        return parse_schedule_html(f.name) # Return the parse_schedule_html function with the temporary file's name
        # and store the parsed results


def test_parse_schedule_html_returns_correct_dicts():
    html = """
    <table>
      <thead>
        <tr>
          <th>Stop A</th>
          <th>Stop B</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>06:00 AM</td>
          <td>06:15 AM</td>
        </tr>
        <tr>
          <td>07:00 AM</td>
          <td>07:15 AM</td>
        </tr>
      </tbody>
    </table>
    """
    results = run_parser_on_html(html) 
    assert len(results) == 2
    assert results[0]["Stop A"] == "06:00 AM"
    assert results[1]["Stop B"] == "07:15 AM"

