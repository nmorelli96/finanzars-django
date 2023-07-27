from django.contrib.auth.models import User
from django.db import models

# Create your models here.

MEP = "MEP"
CCL = "CCL"
ARS = "ARS"
MONEDAS = (
    (MEP, "MEP"),
    (CCL, "CCL"),
    (ARS, "ARS"),
)

CI = "CI"
hs24 = "24hs"
hs48 = "48hs"
PLAZOS = (
    (CI, "CI"),
    (hs24, "24hs"),
    (hs48, "48hs"),
)

class Tipo(models.Model):
    def __str__(self):
        return self.tipo
    tipo = models.CharField(max_length=25)

class Activo(models.Model):
    def __str__(self):
        return f"{self.ticker_ars}"
    
    class Meta:
        verbose_name_plural = "Activos"

    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='activos')
    ticker_ars = models.CharField(max_length=5, blank=False, null=False, help_text='5 caracteres máx.')
    ticker_mep = models.CharField(max_length=5, blank=False, null=False, help_text='5 caracteres máx.')
    ticker_ccl = models.CharField(max_length=5, blank=False, null=False, help_text='5 caracteres máx.')
    nombre = models.CharField(max_length=120, blank=False, null=False)
    mercado = models.CharField(max_length=20, blank=False, null=False)
    ratio = models.FloatField(blank=False, null=False)

class Especie(models.Model):
    def __str__(self):
        return f"{self.especie} - {self.plazo}"
    class Meta:
        ordering = ('tipo', 'especie')
        verbose_name_plural = "Especies"

    especie = models.CharField(max_length=5, blank=False, null=False, help_text='5 caracteres máx.')
    activo = models.ForeignKey(Activo, default=0, on_delete=models.CASCADE, related_name='especies')
    moneda = models.CharField(max_length=3, choices=MONEDAS, default=ARS, blank=False, null=False)
    plazo = models.CharField(max_length=4, choices=PLAZOS, default=hs48, blank=False, null=False)
    ultimo = models.FloatField(blank=False, default=0, null=False)
    var = models.FloatField(default=0.0)
    punta_compra = models.FloatField(default=0.0)
    punta_venta = models.FloatField(default=0.0)
    apertura = models.FloatField(default=0.0)
    maximo = models.FloatField(default=0.0)
    minimo = models.FloatField(default=0.0)
    cierre_ant = models.FloatField(default=0.0)
    volumen = models.IntegerField(default=0)
    monto = models.FloatField(default=0.0)
    hora = models.CharField(max_length=8)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='especies')