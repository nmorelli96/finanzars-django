import pandas as pd
import requests
from instrumento.management.activos_lists import ons_list, ons_mep_list

def scrap_ons():
    html = requests.get('https://bolsar.info/Obligaciones_Negociables.php')
    tables = pd.read_html(html.text, thousands='.', decimal=',')
    ons = tables[0]

    ons = ons.rename(columns={'Especie': "especie"})
    ons['tipo'] = 'ONS'
    ons['moneda'] = 'ARS'
    ons.set_index('especie', inplace=True)
    ons.loc[ons.index.isin(ons_mep_list), 'moneda'] = 'MEP'
    ons['Vto'] = ons['Vto'].str.replace('Cdo.', 'CI')

    return ons[ons.index.isin(ons_list)]
