from django.contrib import admin
from .models import Tipo, Activo, Especie, Especie_USA
from cartera.models import Operacion

admin.site.register(Tipo)
admin.site.register(Especie)
admin.site.register(Activo)
admin.site.register(Operacion)
admin.site.register(Especie_USA)



