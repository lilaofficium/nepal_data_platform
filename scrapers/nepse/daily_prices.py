from scrapers.common.utils import fetch_page
from bs4 import BeautifulSoup

COLUMN_CONFIG = {
    "Symbol": {
        "index": 0,
        "extract": lambda td: td.find("a").get_text(strip=True) if td.find("a") else td.get_text(strip=True)
    },
    "LTP": {
        "index": 1,
        "extract": lambda td: td.get_text(strip=True)
    },
    "Change": {
        "index": 2,
        "extract": lambda td: td.get_text(strip=True)
    },
    "Open": {
        "index": 3,
        "extract": lambda td: td.get_text(strip=True)
    },
    "High": {
        "index": 4,
        "extract": lambda td: td.get_text(strip=True)
    },
    "Low": {
        "index": 5,
        "extract": lambda td: td.get_text(strip=True)
    },
    "Qty": {
        "index": 6,
        "extract": lambda td: td.get_text(strip=True)
    }, 
    "Symbol_Link": {
        "index": 0,
        "extract": lambda td: td.find("a").get("href", "").split("=")[-1] if td.find("a") else ""
    }, 
    "Change_Value": {
        "index": 2,
        "extract": lambda td: float(td.get_text(strip=True)) if td.get_text(strip=True) else 0.0
    }, 
    "Trend": {
        "index": None,   
        "extract": lambda row, col: row.get("class", [""])[0].replace("-row", "") if row.get("class") else ""
    }
}

def main():
    resp = fetch_page("https://merolagani.com/LatestMarket.aspx")
    soup = BeautifulSoup(resp.text, "lxml")
    container = soup.find("div", id="ctl00_ContentPlaceHolder1_LiveTrading")
    table = container.find("table")
    # headers = table.find("thead").find_all("th") 
    all_data=[]
    # header_texts=[]
    # for head in headers:
    #     text = head.get_text(strip=True)
    #     header_texts.append(text)
 
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        col=row.find_all("td") 
        test = {}
        for column_name, config in COLUMN_CONFIG.items():
            idx = config["index"]
            extract_fn = config["extract"]
            if idx is None: 
                test[column_name] = extract_fn(row, col)
            elif idx < len(col): 
                test[column_name] = extract_fn(col[idx])
            else: 
                test[column_name] = ""
        
        all_data.append(test)
        #     if i < len(col):
        #         ## I WANT CUSTOMIZABLE code for all column data also if i wan to define extra 
        #         ## column then it should be allowed how to write code for that
        #         test[h] = col[i].get_text(strip=True)
        # all_data.append(test) 
 
    with open("debug_output_container.txt", "w", encoding="utf-8") as f: 
        for idx, item in enumerate(all_data):
            f.write(f"STEP {idx}:: {str(item)}\n")
                     

if __name__ == "__main__":
    main()  