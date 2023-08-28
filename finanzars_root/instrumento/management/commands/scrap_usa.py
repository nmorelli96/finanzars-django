import json
import pandas as pd
import requests
from datetime import datetime
from instrumento.management.activos_lists import usa_list

def scrap_usa():
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }

    json_data = requests.get(
        'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=100&download=true',
        headers=header,
        timeout=60
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
