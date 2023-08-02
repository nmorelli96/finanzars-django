import pandas as pd
import requests
from management import activos_lists

def scrap_letras():
    html = requests.get('https://bolsar.info/Titulos_Publicos.php')
    tables = pd.read_html(html.text, thousands='.', decimal=',')
    letras = tables[1]

    letras = letras.rename(columns={'Especie': "especie"})
    letras['tipo'] = 'LETRAS'
    letras['moneda'] = 'ARS'
    letras.set_index('especie', inplace=True)
    letras.loc[letras.index.isin(activos_lists.letras_mep_list), 'moneda'] = 'MEP'
    letras['Vto'] = letras['Vto'].str.replace('Cdo.', 'CI')

    return letras[letras.index.isin(activos_lists.letras_list)]
