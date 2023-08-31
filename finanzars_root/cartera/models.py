from django.db import models
from django.contrib.auth.models import User
from instrumento.models import Tipo, Especie, Activo
from django.utils import timezone
from datetime import datetime

COMPRA = "Compra"
VENTA = "Venta"
DIVIDENDO = "Dividendo"
RENTA = "Renta"
AMORTIZACION = "Amortización"
TIPOS_OPERACIONES = (
    (COMPRA, "Compra"),
    (VENTA, "Venta"),
    (DIVIDENDO, "Dividendo"),
    (RENTA, "Renta"),
    (AMORTIZACION, "Amortización"),
)

CI = "CI"
hs24 = "24hs"
hs48 = "48hs"
PLAZOS = (
    (CI, "CI"),
    (hs24, "24hs"),
    (hs48, "48hs"),
)

now = datetime.now()
if 11 > now.hour >= 17:
    now = now.replace(hour=17, minute=0, second=0, microsecond=0)


# Create your models here.
class Operacion(models.Model):
    def __str__(self):
        return f"{self.id} - {self.user.username} - {timezone.localtime(self.fecha)} - {self.get_operacion_display()} - {self.especie}"

    class Meta:
        verbose_name_plural = "Operaciones"

    user = models.ForeignKey(User, related_name="operaciones", on_delete=models.CASCADE)
    tipo = models.ForeignKey(
        Tipo, related_name="operaciones", on_delete=models.DO_NOTHING
    )
    plazo = models.CharField(
        max_length=4, choices=PLAZOS, default=hs48, blank=False, null=False
    )
    activo = models.ForeignKey(
        Activo, default=0, related_name="operaciones", on_delete=models.DO_NOTHING
    )
    especie = models.ForeignKey(
        Especie,
        related_name="operaciones",
        on_delete=models.DO_NOTHING,
    )
    fecha = models.DateTimeField(default=datetime.now)
    cotiz_mep = models.FloatField()
    operacion = models.CharField(
        choices=TIPOS_OPERACIONES, default=COMPRA, max_length=30
    )
    cantidad = models.IntegerField()
    precio_ars = models.FloatField()
    precio_usd = models.FloatField()
    total_ars = models.FloatField(default= 0.0)
    total_usd = models.FloatField(default= 0.0)
    actualizado = models.DateTimeField(default=datetime.now)

    def get_activos_operados(self):
        operaciones = Operacion.objects.all()
        activos_list = []
        for operacion in operaciones:
            activo = operacion.activo
            if activo not in activos_list:
                activos_list.append(activo)

    def calculate_total_ars(self):
        if self.operacion in ["Compra", "Venta"]:
            return self.cantidad * self.precio_ars
        else:
            return self.total_ars

    def calculate_total_usd(self):
        if self.operacion in ["Compra", "Venta"]:
            return self.cantidad * self.precio_usd
        else:
            return self.total_usd
