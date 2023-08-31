from django.db import models
from django.utils import timezone

class Update(models.Model):
    last_update = models.DateTimeField(default=timezone.now)
class Fiat(models.Model):
    data = models.JSONField()

class Banco(models.Model):
    data = models.JSONField()

class Binance(models.Model):
    data = models.JSONField()

class Cryptos(models.Model):
    data = models.JSONField()
