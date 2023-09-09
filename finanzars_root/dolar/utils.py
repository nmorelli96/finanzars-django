from .models import Fiat, Banco, Binance, Cryptos
from instrumento.models import Especie
from django.shortcuts import HttpResponse
import requests
import gc

def fetch_fiat():
    try:
        response = requests.get("https://criptoya.com/api/dolar")
        if response.status_code == 200:
            response_json = response.json()
            if response_json:
                fiat_object, created = Fiat.objects.get_or_create(pk=1)
                fiat_object.data = response_json
                fiat_object.save()
                gc.collect()
                print("Fiat updated")
            else:
                print("No data fetched from API.")
        else:
            print("Unable to fetch Fiat data - HTTP status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Unable to fetch Fiat data -", e)

def fetch_bancos():
    try:
        response = requests.get("https://criptoya.com/api/bancostodos")
        if response.status_code == 200:
            response_json = response.json()
            if response_json:
                bancos_object, created = Banco.objects.get_or_create(pk=1)
                bancos_object.data = response_json
                bancos_object.save()
                gc.collect()
            print("Bancos updated.")
        else:
            print(
                "Unable to fetch Bancos data - HTTP status code:",
                response.status_code,
            )
    except requests.exceptions.RequestException as e:
        print("Unable to fetch Banco data -", e)

def fetch_binance():
    try:
        urls = [
            {"exchange": "Binance", "coin": "USDT", "operation": "buy", "url": "https://criptoya.com/api/binancep2p/buy/usdt/ars/15"},
            {"exchange": "Binance", "coin": "USDT", "operation": "sell", "url": "https://criptoya.com/api/binancep2p/sell/usdt/ars/15"},
            {"exchange": "Binance", "coin": "DAI", "operation": "buy", "url": "https://criptoya.com/api/binancep2p/buy/dai/ars/15"},
            {"exchange": "Binance", "coin": "DAI", "operation": "sell", "url": "https://criptoya.com/api/binancep2p/sell/dai/ars/15"},
        ]

        desired_trade_methods = ["Mercadopago", "Lemon", "Reba", "Banco Brubank", "Belo App", "Uala", "Bank Transfer (Argentina)"]
        response_data = []

        for url in urls:
            response = requests.get(url['url'])
            if response.status_code == 200:
                response_json = response.json()
                original_data = response_json["data"]

                filtered_data = next(
                    (
                        elem
                        for elem in original_data
                        if any(
                            desired_method in method["tradeMethodName"]
                            for method in elem["adv"]["tradeMethods"]
                            for desired_method in desired_trade_methods
                        )
                    ),
                    None,
                )

                if filtered_data:
                    response_json["coin"] = url['coin']
                    response_json["operation"] = url['operation']
                    response_json["data"] = filtered_data
                    response_json["trader"] = filtered_data["advertiser"]["nickName"]
                    response_json["tradeMethod"] = filtered_data["adv"]["tradeMethods"][0]["tradeMethodName"]
                    response_json["price"] = filtered_data["adv"]["price"]
                    del response_json["code"]
                    del response_json["message"]
                    del response_json["messageDetail"]
                    del response_json["data"]
                    response_data.append({url["exchange"]: response_json})
        
                else:
                    print("Filtered data not found in response.")

            else:
                print(
                    "Unable to fetch Binance data - HTTP status code:",
                    response.status_code,
                    )
                    
        binance_data, created = Binance.objects.get_or_create(pk=1)
        binance_data.data = response_data
        #print('binance_data:', binance_data.data)
        binance_data.save()
        del binance_data
        gc.collect()

        print("Binance model updated.")

    except requests.exceptions.RequestException as e:
        print("Unable to fetch Binance data -", e)


def fetch_cryptos():
    try:
        urls = [
            {"exchange": "Belo", "url": "https://criptoya.com/api/belo/usdt/ars"},
            {"exchange": "Buenbit", "url": "https://criptoya.com/api/buenbit/usdt/ars"},
            {"exchange": "Lemon", "url": "https://criptoya.com/api/lemoncash/usdt"},
            {"exchange": "Ripio", "url": "https://criptoya.com/api/ripio/usdt"},
            {"exchange": "SatoshiTango", "url": "https://criptoya.com/api/satoshitango/usdt/ars"},
        ]

        response_data = []
        for url in urls:
            response = requests.get(url['url'])
            if response.status_code == 200:
                response_json = response.json()
                response_data.append({url["exchange"]: response_json})
            else:
                print(
                    "Unable to fetch data from",
                    url,
                    "- HTTP status code:",
                    response.status_code,
                )

        cryptos_data, created = Cryptos.objects.get_or_create(pk=1)
        cryptos_data.data = response_data
        #print('criptos_data:', cryptos_data)
        cryptos_data.save()
        del response_data
        gc.collect()

        print("Cryptos updated.")
    except requests.exceptions.RequestException as e:
        print("Unable to fetch Cryptos data -", e)

def update_data(request):
    fetch_fiat()
    fetch_bancos()
    fetch_binance()
    fetch_cryptos()

    return HttpResponse("Data updated successfully.")

def update_last_data_fiat():
    fiat_data = Fiat.objects.values("data").first()
    fiat_data_last = Fiat.objects.values("data_last").first()
    fiat_data_dict = fiat_data.get("data", {})
    # Reemplazar la data de data_last con la data actualizada de fiat 
    fiat_data_last = fiat_data_dict
    binance_data = Binance.objects.values("data").first()
    # Agregar data de especies
    fiat_data_last['mep_gd30'] = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30D", plazo="48hs")[0].ultimo
    fiat_data_last['ccl_gd30'] = Especie.objects.filter(especie="GD30", plazo="48hs")[0].ultimo / Especie.objects.filter(especie="GD30C", plazo="48hs")[0].ultimo
    fiat_data_last['crypto'] = binance_data["data"][0]["Binance"]["price"]
    # Actualizar fiat_data_last para la columna Var % de Fiat
    fiat_last_object = Fiat.objects.order_by('id').first()
    fiat_last_object.data_last = fiat_data_last
    fiat_last_object.save()
    del fiat_data, fiat_data_last, fiat_data_dict, fiat_last_object
    gc.collect()