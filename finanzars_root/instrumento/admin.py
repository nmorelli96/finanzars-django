from django.contrib import admin
from .models import Tipo, Activo, Especie, Especie_USA, Nasdaq_Data
from cartera.models import Operacion
from cuentas.models import Watchlist, UserProfile
from dolar.models import Fiat, Banco, Binance, Cryptos, Update

class ActivoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticker_ars', 'ticker_mep', 'ticker_ccl', 'ticker_usa', 'tipo', 'nombre', 'ratio', 'vigente',)
    list_filter = ('tipo', 'vigente',) 
    search_fields = ('id', 'ticker_ars', 'ticker_mep', 'ticker_ccl', 'ticker_usa', 'nombre',)

class EspecieAdmin(admin.ModelAdmin):
    list_display = ('id', 'especie', 'activo', 'tipo', 'plazo', 'moneda', 'hora', 'actualizado',)
    list_filter = ('tipo', 'plazo', 'moneda', 'actualizado',) 
    search_fields = ('id', 'especie', 'activo',)

class Especie_USAAdmin(admin.ModelAdmin):
    list_display = ('id', 'especie', 'nombre', 'hora', 'actualizado',)
    search_fields = ('id', 'especie', 'nombre',)

class OperacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tipo', 'plazo', 'activo', 'especie', 'fecha', 'operacion', 'actualizado',)
    list_filter = ('tipo', 'operacion',) 
    search_fields = ('id', 'user', 'activo', 'especie', 'operacion',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_picture_url',)
    search_fields = ('id', 'user',)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'nombre',)
    search_fields = ('id', 'user', 'nombre',)



admin.site.register(Tipo)
admin.site.register(Especie, EspecieAdmin)
admin.site.register(Activo, ActivoAdmin)
admin.site.register(Operacion, OperacionAdmin)
admin.site.register(Especie_USA, Especie_USAAdmin)
admin.site.register(Nasdaq_Data)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Fiat)
admin.site.register(Banco)
admin.site.register(Binance)
admin.site.register(Cryptos)
admin.site.register(Update)
admin.site.register(UserProfile, UserProfileAdmin)




