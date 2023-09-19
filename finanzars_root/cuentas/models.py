from django.db import models
from django.contrib.auth.models import User
from instrumento.models import Especie

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(unique=False, max_length=20)
    especies = models.ManyToManyField(Especie)

    def __str__(self):
        return self.nombre

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.CharField(max_length=200, blank=True, null=True, default="https://i.imgur.com/nkeHzfl.png")

    def __str__(self):
        return self.user.username
