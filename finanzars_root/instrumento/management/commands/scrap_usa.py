import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import glob
from datetime import datetime
from instrumento.management.activos_lists import usa_list

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
#chrome_options.add_argument('user-agent={0}'.format(user_agent)) # para evitar access denied en nasdaq

def scrap_usa():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument('user-agent={0}'.format(user_agent)) # para evitar access denied en nasdaq
    #options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    download_path = r"C:\Users\Nicolas\Documents\REPOS\finanzars-cartera\finanzars_root\instrumento\resources"

    prefs = {
        "download.default_directory": download_path,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get('https://www.nasdaq.com/market-activity/stocks/screener')
    driver.implicitly_wait(15)
    #driver.get_screenshot_as_file("screenshot.png") #check web before finding element
    container = driver.find_element(By.CLASS_NAME, "nasdaq-screener__content-container")
    csv_button = container.find_elements(By.TAG_NAME, "button")
    ActionChains(driver).click(csv_button[0]).perform()
    time.sleep(8)
    driver.close() 

    search_pattern = 'nasdaq_screener'
    file_path = None

    matching_files = []

    for file in os.listdir(download_path):
        if file.startswith(search_pattern):
            matching_files.append(file)
    
    print(matching_files)

    for file in matching_files:
        file_path = os.path.join(download_path, file)
        break

    print(file_path)

    if file_path:
        csv = file_path
        df = pd.read_csv(csv)
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
        df = df.rename(columns={"Symbol": "especie", "Name": "nombre", "Last Sale": "ultimo", "% Change": "var"})

        df_filtered = df[df['especie'].isin(usa_list)]

        df_filtered['ultimo'] = df_filtered['ultimo'].str.replace('$', '').astype(float)
        df_filtered['var'] = df_filtered['var'].str.replace('%', '').astype(float)
        df_filtered['nombre'] = df_filtered['nombre'].str.slice(0, 40)
        df_clean = df_filtered.drop(["Net Change", "Market Cap", "Country", "IPO Year", "Volume", "Sector", "Industry"], axis=1)
        dt_object = datetime.now()
        df_clean['hora'] = dt_object
        df_clean.set_index('especie', inplace=True)
        return df_clean
    else:
        print("No file matching the search pattern was found.")
