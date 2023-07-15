from django import forms
from .models import Especie, Tipo

class NuevaEspecieForm(forms.ModelForm):
      #tipo = forms.ModelChoiceField(queryset=Tipo.objects.all())

      class Meta:
        model = Especie
        fields = ['especie', 'plazo', 'apertura', 
                  'ultimo', 'cierre_ant', 'var', 'hora']
