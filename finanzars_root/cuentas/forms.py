from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
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


class ModificarDatosForm(UserChangeForm):
    
    profile_picture_url = forms.URLField(label='URL de Foto de Perfil', required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
        if self.instance.userprofile.profile_picture_url:
            self.initial['profile_picture_url'] = self.instance.userprofile.profile_picture_url


    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance

        # Validar que el email no esté en uso
        existing_user = User.objects.filter(email=email).exclude(username=user.username).first()
        if existing_user:
            raise forms.ValidationError("El correo electrónico ya está en uso por otro usuario.")
        
        return email
