from django.db import models
from django.contrib.auth.models import User
from instrumento.models import Especie

# Create your models here.
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(unique=True, max_length=20)
    especies = models.ManyToManyField(Especie)

    def __str__(self):
        return self.nombre
