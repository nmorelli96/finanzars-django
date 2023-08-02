from django.forms import CheckboxInput, TextInput
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils import timezone

import django_tables2 as tables
from django_tables2 import A
from django_filters import FilterSet, MultipleChoiceFilter, BooleanFilter, CharFilter
from django.urls import reverse_lazy

from .models import Tipo, Activo, Especie, Especie_USA, PLAZOS

import locale
import babel.numbers
from decimal import Decimal
import datetime

class TiposTable(tables.Table):
    tipo = tables.LinkColumn(
        "especies",
        args=[A("pk")],
        verbose_name="Instrumento",
        attrs={
            "th": {"class": "table-header text-center fw-bold"},
            "td": {"class": "text-center"},
            "a" : {"style": "text-decoration: none; color: forestgreen; font-weight: 500"}
        },
    )

    class Meta:
        model = Tipo
        template_name = "django_tables2/bootstrap5.html"
        fields = ("tipo",)
        attrs = {"class": "table table-striped table-hover"}
        order_by = ("tipo", )


class EspeciesTable(tables.Table):

    favorito = tables.TemplateColumn(
        template_name="includes/agregar_favorito_column.html", empty_values=(),
        orderable=False,
        verbose_name="WL",
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center"},
        },

    )

    especie = tables.Column(
        verbose_name="Especie",
        empty_values=(),
        orderable=True,
        order_by=("especie",),
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-center fw-semibold"},
        },
    )
    plazo = tables.Column(
        verbose_name="Plazo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-center"},
        },
    )
    punta_compra = tables.Column(
        verbose_name="Compra",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-center"},
        },
    )
    punta_venta = tables.Column(
        verbose_name="Venta",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-center"},
        },
    )
    apertura = tables.Column(
        verbose_name="Apertura",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end"},
        },
    )
    cierre_ant = tables.Column(
        verbose_name="Cierre ant.",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end"},
        },
    )
    ultimo = tables.Column(
        verbose_name="Último",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end fw-semibold"},
        },
    )
    var = tables.Column(
        verbose_name="Var %",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end fw-semibold"},
        },
    )
    maximo = tables.Column(
        verbose_name="Máximo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end"},
        },
    )
    minimo = tables.Column(
        verbose_name="Mínimo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end"},
        },
    )
    volumen = tables.Column(
        verbose_name="Volumen",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end"},
        },
    )
    monto = tables.Column(
        verbose_name="Monto Op.",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end"},
        },
    )
    hora = tables.Column(
        verbose_name="Hora",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-center"},
        },
    )

    def render_var(self, value):
        if value is not None:
            value_with_percent = f"{value}%"
            if value < 0:
                return mark_safe(
                    f'<span style="color: red;">{value_with_percent}</span>'
                )
            elif value > 0:
                return mark_safe(
                    f'<span style="color: forestgreen;">{value_with_percent}</span>'
                )
        return value_with_percent

    def render_ultimo(self, value):
        # Configura la configuración regional para Argentina (es_AR)
        #locale.setlocale(locale.LC_ALL, "es_AR")
        # Formatea el número utilizando la configuración regional
        #formatted_value = locale.format_string("%.2f", value, grouping=True)
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value

    def render_apertura(self, value):
        #locale.setlocale(locale.LC_ALL, "es_AR")
        #formatted_value = locale.format_string("%.2f", value, grouping=True)
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value

    def render_cierre_ant(self, value):
        #locale.setlocale(locale.LC_ALL, "es_AR")
        #formatted_value = locale.format_string("%.2f", value, grouping=True)
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value

    def render_punta_compra(self, value):
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value

    def render_punta_venta(self, value):
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value
    
    def render_maximo(self, value):
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value
    
    def render_minimo(self, value):
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value

    def render_volumen(self, value):
        formatted_value = babel.numbers.format_number(value, locale='es_AR')
        return formatted_value

    def render_monto(self, value):
        formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
        return formatted_value


    class Meta:
        model = Especie
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "favorito",
            "especie",
            "plazo",
            "punta_compra",
            "punta_venta",
            "ultimo",
            "var",
            "apertura",
            "maximo",
            "minimo",
            "cierre_ant",
            "volumen",
            "monto",
            "hora",
        )
        attrs = {"class": "table table-striped table-hover table-sm", "id": "especiesTable"}
        empty_text = "No se encontraron especies"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclude = ('id',)



class EspecieFilter(FilterSet):
    plazo = MultipleChoiceFilter(
        field_name="plazo",
        choices=PLAZOS,
    )

    hora = BooleanFilter(
        field_name="hora",
        widget=CheckboxInput(attrs={"class": "btn-check"}),
        label="Operados",
        method="filter_operados",
    )

    especie = CharFilter(lookup_expr='icontains', label='Especie', )

    class Meta:
        model = Especie
        fields = ["plazo", "especie"]

    def filter_plazo(self, queryset, name, value):
        if value == "48hs":
            return queryset.filter(plazo="48hs")
        elif value == "24hs":
            return queryset.filter(plazo="24hs")
        elif value == "CI":
            return queryset.filter(plazo="CI")
        else:
            return queryset

    def filter_operados(self, queryset, name, value):
        if value == "on":
            return queryset.exclude(hora="")
        elif value == "off":
            return queryset
        else:
            return queryset


class EspeciesUsaTable(tables.Table):

    especie = tables.Column(
        verbose_name="Especie",
        empty_values=(),
        orderable=True,
        order_by=("especie",),
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-center fw-semibold text-nowrap"},
        },
    )
    nombre = tables.Column(
        verbose_name="Nombre",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end text-nowrap"},
        },
    )
    ultimo = tables.Column(
        verbose_name="Último",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end fw-semibold text-nowrap"},
        },
    )
    var = tables.Column(
        verbose_name="Var %",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-end fw-semibold text-nowrap"},
        },
    )
    hora = tables.Column(
        verbose_name="Hora",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold"},
            "td": {"class": "text-center text-nowrap"},
        },
    )

    def render_var(self, value):
        if value is not None:
            value_with_percent = f"{value}%"
            if value < 0:
                return mark_safe(
                    f'<span style="color: red;">{value_with_percent}</span>'
                )
            elif value > 0:
                return mark_safe(
                    f'<span style="color: forestgreen;">{value_with_percent}</span>'
                )
        return value_with_percent

    def render_ultimo(self, value):
        formatted_value = babel.numbers.format_currency(value, 'USD', u'#,##0.00', locale='es_AR')
        return formatted_value
    
    def render_hora(self, value):
        hora = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        hora_arg = hora - datetime.timedelta(hours=3)
        formatted_value = hora_arg.strftime("%H:%M:%S")
        tooltip = hora_arg.strftime("%Y-%m-%d %H:%M:%S")
        return format_html('<span title="{}">{}</span>', tooltip, formatted_value)


    class Meta:
        model = Especie_USA
        template_name = "django_tables2/bootstrap5.html"
        fields = (
            "especie",
            "nombre",
            "ultimo",
            "var",
            "hora",
        )
        attrs = {"class": "table table-striped table-hover table-sm", "id": "especiesUsaTable"}
        empty_text = "No se encontraron especies"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclude = ('id',)
