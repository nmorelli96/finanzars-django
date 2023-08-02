
import numpy

def clean_and_export(df, file_name):
    df_clean = df.drop(
        ["Cant. Nominal", "Cant. Nominal.1", "Oper"], axis=1)
    df_clean = df_clean.rename(columns={"Compra": "compra", "Venta": "venta", "Máx": "max", "Mín": "min",
                                        "Volumen": "volumen", "Monto": "monto", "Especie": "especie", "Vto": "plazo",
                                        "Último": "ultimo", "Variación": "var", 'Apertura': 'apertura',
                                        'Cierre Anterior': 'cierre_ant', 'Hora': 'hora'})
    df_clean = df_clean[["moneda", "plazo", "compra", "venta", "ultimo", "var", "apertura", "max", "min", "volumen", "monto", "cierre_ant", "hora", "tipo"]]

    def replace_and_convert(df, *args):
        for arg in args:
            try:
                if arg == 'var':
                    df[arg] = df[arg].str.replace('%', '', regex=True).str.replace(',', '.', regex=False).astype(float)
                elif arg == 'volumen':
                    if df[arg].dtype == 'float64':
                        df[arg] = df[arg].astype(numpy.int64)
                else:
                    if (df[arg].dtype != 'float64') & (df[arg].dtype != 'int64'):
                        df[arg] = df[arg].str.replace('-', '0', regex=False)
                        df[arg] = df[arg].astype(float)
                        '''df[arg] = df[arg].str.replace('.', '', regex=False)
                        df[arg] = df[arg].str.replace(',', '.', regex=False)
                        df[arg] = df[arg].astype(float)'''
            except AttributeError as e:
                print(f"Error in column '{arg}': {e}")


    replace_and_convert(df_clean, 'compra', 'venta', 'ultimo', 'apertura', 'max', 'min', 'cierre_ant', 'volumen', 'monto', 'var')
    print(df_clean)
    df_clean.to_csv(file_name)
