import requests
from bs4 import BeautifulSoup 
import re
from scrapers.common.mongo_client import save_many

BASE_URL = "https://merolagani.com/StockQuote.aspx"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}) 

def fetch_page(url):
    return session.get(url)
 
def extract_hidden_fields(soup): 
    fields = {}
    for inp in soup.find_all("input", type="hidden"):
        name = inp.get("name")
        if name:
            fields[name] = inp.get("value", "")
    return fields


def change_page_index(page_number, soup):  
    form_data = extract_hidden_fields(soup) 
    form_data["ctl00$ContentPlaceHolder1$PagerControl1$hdnCurrentPage"] = str(page_number) 
    btn = soup.find(id="ctl00_ContentPlaceHolder1_PagerControl1_btnPaging")
    btn_name = btn.get("name") if btn else "ctl00$ContentPlaceHolder1$PagerControl1$btnPaging"
    form_data[btn_name] = btn.get("value", "Paging") if btn else "Paging" 
    form_data.setdefault("__EVENTTARGET", "")
    form_data.setdefault("__EVENTARGUMENT", "") 
    resp = session.post(BASE_URL, data=form_data)
    return resp 

def SharePrice():
    resp = fetch_page(BASE_URL)
    soup = BeautifulSoup(resp.text, "lxml")
    span = soup.find("span", id="ctl00_ContentPlaceHolder1_PagerControl1_litRecords")
    if not span:
        return None
    all_data = [] 
    text = span.get_text(strip=True)
    pages = int(re.search(r'Total pages:\s*(\d+)', text).group(1)) 
    for i in range(1, pages + 1):  
      page_resp = change_page_index(i, soup)
      soup_page = BeautifulSoup(page_resp.text, "lxml")  
      with open(f"page_{i}.html", "w", encoding="utf-8") as f:
        f.write(page_resp.text) 
      container = soup_page.find("div", id="ctl00_ContentPlaceHolder1_divData")
      table = container.find("table")
      page_rows = table.find("tbody").find_all("tr")
      for row in page_rows:
        col=row.find_all("td") 
        rowobj = {}
        for column_name, config in Share_Price_COLUMN_CONFIG.items():
            idx = config["index"]
            extract_fn = config["extract"]
            if idx is None: 
                rowobj[column_name] = extract_fn(row, col)
            elif idx < len(col): 
                rowobj[column_name] = extract_fn(col[idx])
            else: 
                rowobj[column_name] = "" 
        all_data.append(rowobj)     

    save_many("nepse_live_Stock_Quote", all_data)



Share_Price_COLUMN_CONFIG ={
"Symbol": {
        "index": 0,
        "extract": lambda td: td.find("a").get_text(strip=True) if td.find("a") else td.get_text(strip=True)
    },
"LTP": {
        "index": 1,
        "extract": lambda td: td.get_text(strip=True)
    },
    "% Change": {
        "index": 2,
        "extract": lambda td: td.get_text(strip=True)
    },
        "High": {
        "index": 4,
        "extract": lambda td: td.get_text(strip=True)
    },     
    "Low":{
        "index": 5,
        "extract": lambda td: td.get_text(strip=True)
    },
    "Open": {
        "index": 5,
        "extract": lambda td: td.get_text(strip=True)
    }, 
    "Qty": {
        "index": 6,
        "extract": lambda td: td.get_text(strip=True)
    } ,
    
        "Turnover": {
        "index": 0,
         "extract": lambda td: td.get_text(strip=True)
    }
} 

