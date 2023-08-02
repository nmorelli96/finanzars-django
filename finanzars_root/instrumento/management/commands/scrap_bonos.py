import pandas as pd
import requests
from management import activos_lists

def scrap_bonos():
    html = requests.get('https://bolsar.info/Titulos_Publicos.php')
    tables = pd.read_html(html.text, thousands='.', decimal=',')
    bonos = tables[0]

    bonos = bonos.rename(columns={'Especie': "especie"})
    bonos['tipo'] = 'BONOS'
    bonos['moneda'] = 'ARS'
    bonos.set_index('especie', inplace=True)
    bonos.loc[bonos.index.isin(activos_lists.bonos_mep_list), 'moneda'] = 'MEP'
    bonos.loc[bonos.index.isin(activos_lists.bonos_ccl_list), 'moneda'] = 'CCL'
    bonos['Vto'] = bonos['Vto'].str.replace('Cdo.', 'CI')

    return bonos[bonos.index.isin(activos_lists.bonos_list)]
