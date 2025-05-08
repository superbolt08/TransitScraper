from scraper.parser import parse_schedule_html
import tempfile

def run_parser_on_html(html_str):
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

def test_parse_schedule_html_empty_table():
    html = "<table><thead></thead><tbody></tbody></table>"
    results = run_parser_on_html(html)
    assert results == []

def test_parse_schedule_html_missing_headers():
    html = "<table><thead></thead><tbody><tr><td>06:00 AM</td></tr></tbody></table>"
    results = run_parser_on_html(html)
    assert results == []

def test_parse_schedule_html_incomplete_row():
    html = """
    <table>
      <thead><tr><th>Stop A</th><th>Stop B</th></tr></thead>
      <tbody><tr><td>06:00 AM</td></tr></tbody>
    </table>
    """
    results = run_parser_on_html(html)
    assert results == []  # Skips invalid/incomplete rows

def test_parse_schedule_html_extra_column():
    html = """
    <table>
      <thead><tr><th>Stop A</th><th>Stop B</th></tr></thead>
      <tbody><tr><td></td><td>06:00 AM</td><td>06:15 AM</td></tr></tbody>
    </table>
    """
    results = run_parser_on_html(html)
    assert len(results) == 1
    assert results[0]["Stop A"] == "06:00 AM"
    assert results[0]["Stop B"] == "06:15 AM"

def test_parse_schedule_html_missing_thead():
    html = """
    <table>
      <tbody>
        <tr><td>06:00 AM</td><td>06:15 AM</td></tr>
      </tbody>
    </table>
    """
    results = run_parser_on_html(html)
    assert results == []

