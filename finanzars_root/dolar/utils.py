from .models import Fiat, Banco, Binance, Cryptos
from django.shortcuts import HttpResponse
import requests

def fetch_fiat():
    try:
        response = requests.get("https://criptoya.com/api/dolar")
        if response.status_code == 200:
            response_json = response.json()
            if response_json:
                fiat_object, created = Fiat.objects.get_or_create(pk=1)
                fiat_object.data = response_json
                fiat_object.save()

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
                            method["tradeMethodName"]
                            in elem["adv"]["tradeMethods"][0]["tradeMethodName"]
                            for method in elem["adv"]["tradeMethods"]
                            if method["tradeMethodName"]
                            in [
                                "Mercadopago",
                                "Lemon",
                                "Reba",
                                "Brubank",
                                "Belo",
                                "Uala",
                            ]
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

        print("Cryptos updated.")
    except requests.exceptions.RequestException as e:
        print("Unable to fetch Cryptos data -", e)

def update_data(request):
    fetch_fiat()
    fetch_bancos()
    fetch_binance()
    fetch_cryptos()

    return HttpResponse("Data updated successfully.")
