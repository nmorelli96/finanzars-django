from django.shortcuts import render
from .tables import BancosTable, FiatTable, CryptosTable
import requests
from collections import namedtuple
from datetime import datetime

# Create your views here.

def DolarView(request):
    response_bancos = requests.get('https://finanzars-dolar.onrender.com/getBancos')
    bancos_data = response_bancos.json()
    Banco = namedtuple("Banco", ["banco", "compra", "venta", "ventaTot", "hora"])

    bancos_mapping = {
        "Balanz": "balanz",
        "Hipotecario": "hipotecario",
        "ICBC": "icbc",
        "Supervielle": "supervielle",
        "Brubank": "brubank",
        "Ciudad": "ciudad",
        "Provincia": "bapro",
        "HSBC": "hsbc",
        "Macro": "macro",
        "Patagonia": "patagonia",
        "BBVA": "bbva",
        "Galicia": "galicia",
        "Santander": "santander",
        "Reba": "rebanking",
        "Nación": "bna",
        "CambioAR": "cambioar",
        "Plus": "plus"
    }

    bancos = []
    for banco_data in bancos_data:
        for key, value in banco_data.items():
            if key == "rebanking":
                continue
            elif key != "_id":
                banco_nombre = next((k for k, v in bancos_mapping.items() if v == key), key)
                banco = Banco(
                    banco=banco_nombre,
                    compra=value.get("ask"),
                    venta=value.get("bid"),
                    ventaTot=value.get("totalAsk"),
                    hora=value.get("time")
                )
                bancos.append(banco)

    bancos_table = BancosTable(bancos, order_by=request.GET.get("sort"))


    response_fiat = requests.get('https://finanzars-dolar.onrender.com/getFiat')
    fiat_data = response_fiat.json()
    Fiat = namedtuple("Fiat", ["dolar", "venta"])
    fiatHora = datetime.fromtimestamp(fiat_data[0]['time']).strftime("%H:%M")

    fiat = [Fiat(dolar='Oficial', venta=fiat_data[0]["oficial"]), 
            Fiat(dolar='Solidario', venta=fiat_data[0]["solidario"]),
            Fiat(dolar='Blue', venta=fiat_data[0]["blue"]),
            Fiat(dolar='MEP', venta=fiat_data[0]["mep"]),
            Fiat(dolar='CCL', venta=fiat_data[0]["ccl"])]

    fiat_table = FiatTable(fiat, order_by=request.GET.get("sort"))


    response_cryptos = requests.get('https://finanzars-dolar.onrender.com/getCryptos')
    cryptos_data = response_cryptos.json()
    Crypto = namedtuple("Crypto", ["banco", "coin", "compra", "venta", "hora"])

    cryptos = []
    for crypto_data in cryptos_data:
        for crypto in crypto_data["cryptos"]:
            banco = crypto["banco"]
            coin = crypto["coin"]
            compra = crypto["compra"]
            venta = crypto["venta"]
            hora = crypto["time"]

            crypto_item = Crypto(
                banco=banco,
                coin=coin,
                compra=compra,
                venta=venta,
                hora=hora
            )
            cryptos.append(crypto_item)

    binance_urls = [
        "https://finanzars-dolar.onrender.com/getBinanceUSDTs",
        "https://finanzars-dolar.onrender.com/getBinanceUSDTb",
        "https://finanzars-dolar.onrender.com/getBinanceDAIs",
        "https://finanzars-dolar.onrender.com/getBinanceDAIb"
    ]

    for url in binance_urls:
        response = requests.get(url)
        binance_data = response.json()

        for binance_item in binance_data:
            banco = "Binance P2P"
            coin = None
            if "USDT" in url:
                coin = "USDT"
            elif "DAI" in url:
                coin = "DAI"

            hora = binance_item["time"]
            crypto_item = next((crypto for crypto in cryptos if crypto.hora == hora and crypto.coin == coin), None)
            
            if crypto_item is None:
                crypto_item = Crypto(
                    banco=banco,
                    coin=coin,
                    compra=None,
                    venta=None,
                    hora=hora,
                )
                cryptos.append(crypto_item)

            if "b" in url[-1]:
                crypto_item = crypto_item._replace(compra=binance_item["price"])
            elif "s" in url[-1]:
                crypto_item = crypto_item._replace(venta=binance_item["price"])

            # Actualizar el elemento en la lista
            cryptos = [c if c.hora != hora or c.coin != coin else crypto_item for c in cryptos]


    cryptos_table = CryptosTable(cryptos, order_by=request.GET.get("sort"))

    return render(request, 'dolar.html', {'bancos_table': bancos_table, 'fiat_table': fiat_table, 'fiatHora': fiatHora, 'cryptos_table': cryptos_table})
