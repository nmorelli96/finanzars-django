import pandas as pd
import requests
from instrumento.management.activos_lists import cedears_list, cedears_mep_list

def scrap_cedears():
    html = requests.get('http://bolsar.info/Cedears.php')
    tables = pd.read_html(html.text, thousands='.', decimal=',')
    cedears = tables[0]

    cedears = cedears.rename(columns={'Especie': "especie"})
    cedears['tipo'] = 'CEDEARS'
    cedears['moneda'] = 'ARS'
    cedears.set_index('especie', inplace=True)
    cedears.loc[cedears.index.isin(cedears_mep_list), 'moneda'] = 'MEP'
    cedears['Vto'] = cedears['Vto'].str.replace('Cdo.', 'CI')

    return cedears[cedears.index.isin(cedears_list)]

