from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from cuentas.models import Watchlist

class RegistroForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class WatchlistForm(forms.ModelForm):
    nombre = forms.CharField(label='Nombre', max_length=20)

    class Meta:
        model = Watchlist
        fields = ('nombre',)
