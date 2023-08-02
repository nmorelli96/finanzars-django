import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
from datetime import datetime
from management import activos_lists

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--no-sandbox')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument('user-agent={0}'.format(user_agent)) # para evitar access denied en nasdaq

def scrap_usa():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.nasdaq.com/market-activity/stocks/screener')
    driver.implicitly_wait(15)
    #driver.get_screenshot_as_file("screenshot.png") #check web before finding element
    container = driver.find_element(By.CLASS_NAME, "nasdaq-screener__content-container")
    csv_button = container.find_elements(By.TAG_NAME, "button")
    ActionChains(driver).click(csv_button[0]).perform()
    time.sleep(10)

    search_pattern = 'nasdaq_screener*'
    file_path = None

    for file in glob.glob(search_pattern):
        file_path = file
        break

    if file_path:
        csv = file
        df = pd.read_csv(csv)
        df = df.rename(columns={"Symbol": "especie", "Name": "nombre", "Last Sale": "ultimo", "% Change": "var"})

        df_filtered = df[df['especie'].isin(activos_lists.usa_list)]

        df_filtered['ultimo'] = df_filtered['ultimo'].str.replace('$', '').astype(float)
        df_filtered['var'] = df_filtered['var'].str.replace('%', '').astype(float)
        df_filtered['nombre'] = df_filtered['nombre'].str.slice(0, 40)
        df_clean = df_filtered.drop(["Net Change", "Market Cap", "Country", "IPO Year", "Volume", "Sector", "Industry"], axis=1)
        timestamp = int(csv[16:29])
        dt_object = datetime.fromtimestamp(timestamp / 1000)
        df_clean['hora'] = dt_object
        df_clean.set_index('especie', inplace=True)
        df_clean
        df_clean.to_csv('usa.csv')
        driver.implicitly_wait(2)
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
    else:
        print("No file matching the search pattern was found.")
