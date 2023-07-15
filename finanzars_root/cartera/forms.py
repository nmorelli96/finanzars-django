from django import forms
from .models import Operacion
from instrumento.models import Especie, Activo


class NuevaOperacionForm(forms.ModelForm):
    # tipo = forms.ModelChoiceField(queryset=Tipo.objects.all())

    class Meta:
        model = Operacion
        fields = [
            "plazo",
            "tipo",
            "activo",
            "especie",
            "fecha",
            "cotiz_mep",
            "operacion",
            "cantidad",
            "precio_ars",
            "precio_usd",
        ]
        labels = {
            "plazo": "Plazo de liquidación",
            "tipo": "Tipo",
            "activo": "Activo",
            "especie": "Especie (Ticker con moneda la correspondiente)",
            "fecha": "Fecha / Hora",
            "cotiz_mep": "Cotización MEP",
            "operacion": "Operación",
            "cantidad": "Cantidad",
            "precio_ars": "Precio en ARS",
            "precio_usd": "Precio en USD",
        }
        widgets = {
            "fecha": forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['especie'].queryset = Especie.objects.none()
        self.fields['activo'].queryset = Activo.objects.none()

        if 'tipo' in self.data:
            try:
                tipo_id = int(self.data.get('tipo'))
                self.fields['activo'].queryset = Activo.objects.filter(tipo_id=tipo_id).order_by('ticker_ars')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Activo queryset
        elif self.instance.pk:
            self.fields['activo'].queryset = self.instance.tipo.activos.order_by('ticker_ars')

        if 'activo' in self.data:
            try:
                activo_id = int(self.data.get('activo'))
                self.fields['especie'].queryset = Especie.objects.filter(activo_id=activo_id).order_by('especie')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Activo queryset
        elif self.instance.pk:
            self.fields['especie'].queryset = self.instance.activo.especies.order_by('especie')

