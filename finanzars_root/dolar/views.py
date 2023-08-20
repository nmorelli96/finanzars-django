from django.shortcuts import render, redirect
from .utils import update_data
import requests
from collections import namedtuple
from datetime import datetime, timedelta
from django.utils import timezone
from .tables import BancosTable, FiatTable, CryptosTable
import dolar.models as models

def DolarView(request):
    time_zone = timezone.get_current_timezone()
    updated = models.Update.objects.first()
    current_time = datetime.now().replace(tzinfo=time_zone)
    last_updated = updated.last_update.replace(tzinfo=time_zone)

    time_since_last_update = current_time - last_updated

    #print('current', current_time)
    #print('updated', last_updated)
    #print(time_since_last_update)
    #print(time_since_last_update > timedelta(minutes=5))

    if time_since_last_update > timedelta(minutes=5):
        update_data(request)
        updated.last_update = current_time - timedelta(hours=3)
        updated.save()
    
    bancos_data = models.Banco.objects.all().values()
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
        "Plus": "plus",
    }

    bancos = []
    for banco_data in bancos_data:
        banco_data_dict = banco_data.get("data", {})
        for key, value in banco_data_dict.items():
            if key in ["rebanking", "buendolar", "globalcambio", "naranjax", "dolaria", "dolariol", "cambioposadas", "prex", "cambiodieza", "davsa", "triacambio", "plazacambio", "cambiosroca"]:
                continue
            elif key != "_id":
                banco_nombre = next(
                    (k for k, v in bancos_mapping.items() if v == key), key
                )
                banco = Banco(
                    banco=banco_nombre,
                    compra=value.get("bid"),
                    venta=value.get("totalAsk") / 1.75,
                    ventaTot=value.get("totalAsk"),
                    hora=value.get("time"),
                )
                bancos.append(banco)

    bancos_table = BancosTable(bancos, order_by=request.GET.get("sort"))


    fiat_data = models.Fiat.objects.values("data").first()
    fiat_data_dict = fiat_data.get("data", {})
    Fiat = namedtuple("Fiat", ["dolar", "venta"])
    fiatHora = datetime.fromtimestamp(fiat_data_dict["time"]).strftime("%Y-%m-%d %H:%M:%S")

    fiat = [
        Fiat(dolar="Oficial", venta=fiat_data_dict["oficial"]),
        Fiat(dolar="Solidario", venta=fiat_data_dict["solidario"]),
        Fiat(dolar="Blue", venta=fiat_data_dict["blue"]),
        Fiat(dolar="MEP", venta=fiat_data_dict["mep"]),
        Fiat(dolar="CCL", venta=fiat_data_dict["ccl"]),
    ]

    fiat_table = FiatTable(fiat)


    cryptos_data = models.Cryptos.objects.values("data").first()
    cryptos_data_dict = cryptos_data.get("data", {})
    Crypto = namedtuple("Crypto", ["banco", "coin", "compra", "venta", "hora"])

    cryptos = []
    for crypto_dict in cryptos_data_dict:
        for banco, data in crypto_dict.items():
            compra = data["totalAsk"]
            venta = data["totalBid"]
            hora = data["time"]
            coin = "USDT"

            crypto_item = Crypto(
                banco=banco,
                coin=coin,
                venta=compra,
                compra=venta,
                hora=hora
            )
            cryptos.append(crypto_item)

    binance_data = models.Binance.objects.values("data").first()
    binance_data_dict = binance_data.get("data", [])

    binance_dai_item = Crypto(
                    banco='Binance P2P',
                    coin='DAI',
                    compra=None,
                    venta=None,
                    hora=None,)
    
    binance_usdt_item = Crypto(
                banco='Binance P2P',
                coin='USDT',
                compra=None,
                venta=None,
                hora=None,)

    for binance_dict in binance_data_dict:
        try:
            data = binance_dict.get("Binance", {})
            coin = data.get("coin", "")
            hora = data.get("time", 0)
            #trader = data.get("trader", "")
            #trade_method = data.get("tradeMethod", "")
            price = float(data.get("price", 0))

            if coin == 'USDT':
                if data["operation"] == 'buy':
                    binance_usdt_item = binance_usdt_item._replace(venta=price, hora=hora)
                else:
                    binance_usdt_item = binance_usdt_item._replace(compra=price)
            elif coin == 'DAI':
                if data["operation"] == 'buy':
                    binance_dai_item = binance_dai_item._replace(venta=price, hora=hora)
                else:
                    binance_dai_item = binance_dai_item._replace(compra=price)

        
            #cryptos = [
            #    c if c.hora != hora or c.coin != coin else crypto_item for c in cryptos
            #]

        except models.Binance.DoesNotExist:
            print("Binance data does not exist in the database.")
    
    cryptos.append(binance_usdt_item)
    cryptos.append(binance_dai_item)

    cryptos_table = CryptosTable(cryptos, order_by=request.GET.get("sort"))

    return render(
        request,
        "dolar.html",
        {
            "bancos_table": bancos_table,
            "fiat_table": fiat_table,
            "fiatHora": fiatHora,
            "cryptos_table": cryptos_table,
        },
    )


def DolarFetch(request):
    update_data(request)
    return redirect('dolar')
