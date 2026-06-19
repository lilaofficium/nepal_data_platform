import requests
from bs4 import BeautifulSoup 
import time

BASE_URL = "https://merolagani.com/StockQuote.aspx"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": BASE_URL,
}

def get_hidden_fields(soup):
    """Extract ASP.NET hidden fields needed for postback."""
    fields = {}
    for hidden in soup.find_all("input", type="hidden"):
        name = hidden.get("name")
        value = hidden.get("value", "")
        if name:
            fields[name] = value
    return fields

def parse_table(soup):
    """Parse the stock data table into a list of dicts."""
    table = soup.find("div", id="ctl00_ContentPlaceHolder1_divData")
    if not table:
        return []
    rows = []
    for tr in table.find_all("tr")[1:]:  # skip header
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cols) >= 8:
            rows.append({
                "#": cols[0],
                "Symbol": cols[1],
                "LTP": cols[2],
                "% Change": cols[3],
                "High": cols[4],
                "Low": cols[5],
                "Open": cols[6],
                "Qty": cols[7],
                "Turnover": cols[8] if len(cols) > 8 else "",
            })
    return rows

def scrape_all_pages():
    session = requests.Session()
    all_data = []

    # --- Page 1: GET request ---
    resp = session.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")

    all_data.extend(parse_table(soup))
    hidden = get_hidden_fields(soup)

    # Find total pages
    # Look for pagination links like "Page 2", "Page 3" etc.
    pagination = soup.find_all("a", title=lambda t: t and t.startswith("Page "))
    total_pages = len(pagination) + 1  # +1 for current page
    print(f"Total pages found: {total_pages}")
 
    for page_num in range(2, total_pages + 1):
        print(f"Scraping page {page_num}...")
 
        payload = {
            **hidden,
            "__EVENTTARGET": f"ctl00$ContentPlaceHolder1$ASPxGridView1",
            "__EVENTARGUMENT": f"PBN|{page_num}",   
        }

        resp = session.post(BASE_URL, data=payload, headers=HEADERS)
        soup = BeautifulSoup(resp.text, "html.parser")

        rows = parse_table(soup)
        if not rows:
            print(f"  No data on page {page_num}, stopping.")
            break

        all_data.extend(rows)
        hidden = get_hidden_fields(soup)  # Update ViewState for next POST
        time.sleep(1)  # Be polite

    return all_data

data = scrape_all_pages()  
print("Saved to nepse_stockquote.csv")