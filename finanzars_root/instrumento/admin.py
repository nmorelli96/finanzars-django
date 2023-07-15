from django.contrib import admin
from .models import Tipo, Especie, Activo
from cartera.models import Operacion

admin.site.register(Tipo)
admin.site.register(Especie)
admin.site.register(Activo)
admin.site.register(Operacion)


