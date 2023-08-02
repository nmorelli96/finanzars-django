import pandas as pd
import requests
from management import activos_lists

def scrap_cedears():
    html = requests.get('http://bolsar.info/Cedears.php')
    tables = pd.read_html(html.text, thousands='.', decimal=',')
    cedears = tables[0]

    cedears = cedears.rename(columns={'Especie': "especie"})
    cedears['tipo'] = 'CEDEARS'
    cedears['moneda'] = 'ARS'
    cedears.set_index('especie', inplace=True)
    cedears.loc[cedears.index.isin(activos_lists.cedears_mep_list), 'moneda'] = 'MEP'
    cedears['Vto'] = cedears['Vto'].str.replace('Cdo.', 'CI')

    return cedears[cedears.index.isin(activos_lists.cedears_list)]

