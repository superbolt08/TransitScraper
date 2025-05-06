from scraper.parser import parse_schedule_html
from bs4 import BeautifulSoup
import tempfile

sample_html = """
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

def test_parse_schedule_html_returns_correct_dicts():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.html', delete=False) as f:
        f.write(sample_html)
        f.seek(0)
        results = parse_schedule_html(f.name)

    assert len(results) == 2
    assert results[0]["Stop A"] == "06:00 AM"
    assert results[1]["Stop B"] == "07:15 AM"
