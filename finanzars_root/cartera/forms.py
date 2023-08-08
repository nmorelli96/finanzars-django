from django import forms
from .models import Operacion
from instrumento.models import Especie, Activo
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError


class NuevaOperacionForm(forms.ModelForm):

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
            "total_ars",
            "total_usd"
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
            "total_ars": "Total en ARS",
            "total_usd": "Total en USD",

        }
        widgets = {
            "fecha": forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': '60'})
        }

    def __init__(self, *args, is_new=True, activos_en_tenencia=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_new = is_new

        self.activos_en_tenencia = activos_en_tenencia

        self.fields['cotiz_mep'].widget.attrs['id'] = 'cotiz_mep_field'
        self.fields['operacion'].widget.attrs['id'] = 'operacion_field'
        self.fields['cantidad'].widget.attrs['id'] = 'cantidad_field'
        self.fields['precio_ars'].widget.attrs['id'] = 'precio_ars_field'
        self.fields['precio_usd'].widget.attrs['id'] = 'precio_usd_field'
        self.fields['total_ars'].widget.attrs['id'] = 'total_ars_field'
        self.fields['total_usd'].widget.attrs['id'] = 'total_usd_field'


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

        # Seteo del field hora
        if is_new:
            # Si es una operación nueva
            default_datetime = datetime.now()
            if not (11 <= default_datetime.hour <= 17):
                if default_datetime.hour < 11:
                    default_datetime -= timedelta(days=1, hours=default_datetime.hour, minutes=default_datetime.minute)
                    default_datetime = default_datetime.replace(hour=17, minute=0)
                else:
                    default_datetime = default_datetime.replace(hour=17, minute=0)
            
            self.initial={'fecha': default_datetime.strftime('%Y-%m-%dT%H:%M')}

            # Establecer los valores de totales predeterminados a 0.0
            self.fields['total_ars'].initial = 0.0
            self.fields['total_usd'].initial = 0.0

        else:
            # Si es una operación existente
            fecha = timezone.localtime(kwargs["instance"].fecha)
            self.initial={'fecha': fecha.strftime('%Y-%m-%dT%H:%M')}

            # Establecer los valores de totales predeterminados desde la instancia
            self.fields['total_ars'].initial = self.instance.total_ars
            self.fields['total_usd'].initial = self.instance.total_usd


    def clean_cotiz_mep(self):
        cotiz_mep = self.cleaned_data.get('cotiz_mep')
        if cotiz_mep is not None and cotiz_mep < 0:
            raise ValidationError('La cotización MEP debe ser un valor positivo o cero.')
        return cotiz_mep

    def clean_cantidad(self):
        cantidad_a_vender = self.cleaned_data.get('cantidad')
        
        if cantidad_a_vender is not None and cantidad_a_vender < 0:
            raise ValidationError('La cantidad debe ser un valor positivo o cero.')
        
        if self.cleaned_data.get('operacion') == 'Venta':
            activo_a_vender = self.cleaned_data.get('activo')
            
            activos_en_tenencia = self.activos_en_tenencia
            activo_deseado = None

            print("Activo a vender:", activo_a_vender)
            for activo in activos_en_tenencia:
                print(activo['ticker_ars'])
                if activo['ticker_ars'] == activo_a_vender.ticker_ars:
                    activo_deseado = activo
                    print("Cantidad de activo deseado encontrado:", activo_deseado['cantidad'])
                    break
            if activo_deseado is not None and activo_deseado["cantidad"] < cantidad_a_vender:
                raise forms.ValidationError("No hay suficiente cantidad de ese activo para realizar la venta.")
        
        return cantidad_a_vender

    def clean_precio_ars(self):
        precio_ars = self.cleaned_data.get('precio_ars')
        if precio_ars is not None and precio_ars < 0:
            raise ValidationError('El precio en ARS debe ser un valor positivo o cero.')
        return precio_ars

    def clean_precio_usd(self):
        precio_usd = self.cleaned_data.get('precio_usd')
        if precio_usd is not None and precio_usd < 0:
            raise ValidationError('El precio en USD debe ser un valor positivo o cero.')
        return precio_usd
