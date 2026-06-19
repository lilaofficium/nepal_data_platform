from scrapers.common.utils import fetch_page
from bs4 import BeautifulSoup
from scrapers.common.mongo_client import save_many
from scrapers.nepse.StockQuote import SharePrice

LIVE_TRADING_COLUMN_CONFIG = {
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

LIVE_GAINERS_COLUMN_CONFIG ={
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
        "extract": lambda td: float(td.get_text(strip=True)) if td.get_text(strip=True) else 0.0
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
    } 
}


LIVE_TURNOVERS_COLUMN_CONFIG ={
    "Symbol": {
        "index": 0,
        "extract": lambda td: td.find("a").get_text(strip=True) if td.find("a") else td.get_text(strip=True)
    },
        "Turnover": {
        "index": 0,
         "extract": lambda td: td.get_text(strip=True)
    },
        "LTP": {
        "index": 0,
        "extract": lambda td: td.get_text(strip=True)
    }
}


def main():
    resp = fetch_page("https://merolagani.com/LatestMarket.aspx")
    soup = BeautifulSoup(resp.text, "lxml")   
    # LiveTrading(soup)   
    # LiveGainers(soup)
    # LiveLosers(soup)
    # TopTurnovers(soup)
    SharePrice()
def LiveTrading(soup):
    container = soup.find("div", id="ctl00_ContentPlaceHolder1_LiveTrading")
    table = container.find("table")  
    all_data=[]  
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        col=row.find_all("td") 
        rowobj = {}
        for column_name, config in LIVE_TRADING_COLUMN_CONFIG.items():
            idx = config["index"]
            extract_fn = config["extract"]
            if idx is None: 
                rowobj[column_name] = extract_fn(row, col)
            elif idx < len(col): 
                rowobj[column_name] = extract_fn(col[idx])
            else: 
                rowobj[column_name] = "" 
        all_data.append(rowobj) 
    save_many("nepse_live_trading", all_data)   

def LiveGainers(soup):
    container = soup.find("div", id="ctl00_ContentPlaceHolder1_LiveTrading")
    table = container.find("table")  
    all_data=[]  
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        col=row.find_all("td") 
        rowobj = {}
        for column_name, config in LIVE_GAINERS_COLUMN_CONFIG.items():
            idx = config["index"]
            extract_fn = config["extract"]
            if idx is None: 
                rowobj[column_name] = extract_fn(row, col)
            elif idx < len(col): 
                rowobj[column_name] = extract_fn(col[idx])
            else: 
                rowobj[column_name] = "" 
        all_data.append(rowobj) 
    save_many("nepse_live_gainers", all_data)    
   
def LiveLosers(soup):
    container = soup.find("div", id="ctl00_ContentPlaceHolder1_LiveLosers")
    if not container:
        print("ERROR: Container not found")
        return
    
    table = container.find("table")
    if not table:
        print("ERROR: Table not found")
        return
     
    tbody = table.find("tbody")
    if tbody:
        rows = tbody.find_all("tr")
        print(f"Found {len(rows)} rows in <tbody>")
    else:
        rows = table.find_all("tr")
        print(f"No <tbody> found. Found {len(rows)} rows directly in <table>")
    
    if not rows:
        print("ERROR: No rows found at all")
        return
    
    all_data = []
    for row in rows:
        col = row.find_all("td")
        if not col:
            continue  # Skip header rows (they have <th>)
        
        rowobj = {}
        for column_name, config in LIVE_GAINERS_COLUMN_CONFIG.items():
            idx = config["index"]
            extract_fn = config["extract"]
            if idx is None:
                rowobj[column_name] = extract_fn(row, col)
            elif idx < len(col):
                rowobj[column_name] = extract_fn(col[idx])
            else:
                rowobj[column_name] = ""
        all_data.append(rowobj)
    
    print(f"Successfully parsed {len(all_data)} rows")
    save_many("nepse_live_losers", all_data)


def TopTurnovers(soup):
    container = soup.find("div", id="ctl00_ContentPlaceHolder1_LiveTurnovers")
    if not container:
        print("ERROR: Container not found")
        return
    
    table = container.find("table")
    if not table:
        print("ERROR: Table not found")
        return
     
    tbody = table.find("tbody")
    if tbody:
        rows = tbody.find_all("tr")
        print(f"Found {len(rows)} rows in <tbody>")
    else:
        rows = table.find_all("tr")
        print(f"No <tbody> found. Found {len(rows)} rows directly in <table>")
    
    if not rows:
        print("ERROR: No rows found at all")
        return
    
    all_data = []
    for row in rows:
        col = row.find_all("td")
        if not col:
            continue  # Skip header rows (they have <th>)
        
        rowobj = {}
        for column_name, config in LIVE_TURNOVERS_COLUMN_CONFIG.items():
            idx = config["index"]
            extract_fn = config["extract"]
            if idx is None:
                rowobj[column_name] = extract_fn(row, col)
            elif idx < len(col):
                rowobj[column_name] = extract_fn(col[idx])
            else:
                rowobj[column_name] = ""
        all_data.append(rowobj)
    
    print(f"Successfully parsed {len(all_data)} rows")
    save_many("nepse_live_turn_overs", all_data)


 


#####################        
if __name__ == "__main__":
    main()  