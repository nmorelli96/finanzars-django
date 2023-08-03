import pandas as pd
import requests
from instrumento.management.activos_lists import merval_list

def scrap_merval():
    html = requests.get('https://bolsar.info/paneles.php?panel=2&titulo=Panel%20General')
    tables = pd.read_html(html.text, thousands='.', decimal=',')
    panel_general = tables[0]

    html = requests.get('https://bolsar.info/lideres.php')
    tables = pd.read_html(html.text, thousands='.', decimal=',')
    panel_lideres = tables[0]

    panel_lideres = panel_lideres.rename(columns={'Max': "Máx"})
    merval = pd.concat([panel_lideres, panel_general], ignore_index=True)

    merval = merval.rename(columns={'Especie': "especie"})
    merval['tipo'] = 'MERVAL'
    merval['moneda'] = 'ARS'
    merval.set_index('especie', inplace=True)
    merval['Vto'] = merval['Vto'].str.replace('Cdo.', 'CI')

    return merval[merval.index.isin(merval_list)]