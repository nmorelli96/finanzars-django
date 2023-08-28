import json
import pandas as pd
import requests
from datetime import datetime

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
#chrome_options.add_argument('user-agent={0}'.format(user_agent)) # para evitar access denied en nasdaq

def scrap_usa():
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }

    usa_list = ["AMZN", "AAPL", "GOOGL", "KO", "NIO", "COIN", "PBR", "BB", "AMD", "BABA", "DIS", "MELI", "VIST", "TSLA", "SHOP", "MSFT", "JNJ", "BBD", "INTC", "AGRO", "NKE", "NVDA", "HMY", "UPST", "VALE", "AXP", "TS", "OXY", "BRK/B", "T", "ABNB", "ARCO", "GOLD", "META", "BRFS", "PYPL", "BITF", "SE", "X", "GLOB", "PFE", "PAAS", "BAC", "SATL", "ZM", "JMIA", "CAAP", "WMT", "C", "HUT", "JPM", "ETSY", "QCOM", "XOM", "PG", "TGT", "ERJ", "MMM", "WFC", "JD", "TEF", "ITUB", "VZ", "GE", "MO", "MCD", "WBA", "HD", "AZN", "ERIC", "COST", "V", "HSY", "CDE", "CVX", "TWLO", "TSM", "SPOT", "NFLX", "SQ", "TRIP", "CAT", "TX", "CRM", "BA", "BIDU", "BG", "DOCU", "PEP", "DESP", "ADBE", "FSLR", "GM", "MU", "AAL", "UNH", "LYG", "BIOX", "MOS", "NUE", "LRCX", "RIO", "IBM", "ABBV", "SBS", "PSX", "NG", "ABEV", "UAL", "F", "UL", "GGB", "FCX", "MSTR", "AIG", "CSCO", "MA", "AMGN", "BP", "XP", "HOG", "CBD", "PHG", "SONY", "DE", "SBUX", "LMT", "UGP", "SHEL", "MRK", "CX", "USB", "SID", "SNOW", "NEM", "TXN", "GSK", "PANW", "BBVA", "ABT", "NOK", "MSI", "TMO", "DOW", "EBAY", "HON", "SPGI", "YY", "RBLX", "INFY", "FDX", "SNAP", "SAN", "ORCL", "LLY", "ADI", "TM", "GS", "DD", "BHP", "EBR", "HL", "NTES", "HAL", "VOD", "NTCO", "PKX", "AEM", "GLW", "UBER", "GPRK", "TTE", "SLB", "AMAT", "UNP", "GILD", "GFI", "WB", "RTX", "BIIB", "ELP", "PBI", "XRX", "ORAN", "HDB", "SYY", "BSBR", "TV", "EA", "HSBC", "AVY", "BK", "CL", "CAH", "AKO/B", "MDT", "E", "KMB", "SCCO", "IBN", "KB", "GRMN", ]

    json_data = requests.get(
        'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=100&download=true',
        headers=header,
        timeout=30
    )

    data = json.loads(json_data.text)
    rows = data["data"]["rows"]

    df = pd.DataFrame(rows)

    df["lastsale"] = df["lastsale"].str.replace("$", "").astype(float)
    df["pctchange"] = df["pctchange"].str.replace("%", "").astype(float)
    df["name"] = df["name"].str.slice(0, 40)
    df.rename(columns={"symbol": "especie", "name": "nombre", "lastsale": "ultimo", "pctchange": "var"}, inplace=True)
    df_filtered = df[df['especie'].isin(usa_list)]
    df_clean = df_filtered.drop(["netchange", "marketCap", "country", "ipoyear", "volume", "sector", "industry", "url"], axis=1)
    dt_object = datetime.now()
    df_clean['hora'] = dt_object
    df_clean.set_index("especie", inplace=True)

    return df_clean
