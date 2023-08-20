from django.contrib import admin
from .models import Tipo, Activo, Especie, Especie_USA
from cartera.models import Operacion
from cuentas.models import Watchlist
from dolar.models import Fiat, Banco, Binance, Cryptos, Update


admin.site.register(Tipo)
admin.site.register(Especie)
admin.site.register(Activo)
admin.site.register(Operacion)
admin.site.register(Especie_USA)
admin.site.register(Watchlist)
admin.site.register(Fiat)
admin.site.register(Banco)
admin.site.register(Binance)
admin.site.register(Cryptos)
admin.site.register(Update)





