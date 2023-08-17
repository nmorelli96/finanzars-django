from django.forms import CheckboxInput, TextInput
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils import timezone

import django_tables2 as tables
from django_tables2 import A
from django_filters import FilterSet, MultipleChoiceFilter, BooleanFilter, CharFilter
from django.urls import reverse_lazy

from .models import Tipo, Activo, Especie, Especie_USA, PLAZOS

import babel.numbers
import datetime


class TiposTable(tables.Table):
    tipo = tables.TemplateColumn(
        '<a href="{% url "especies" record.pk %}?plazo=48hs">{{ record.tipo }}</a>',
        verbose_name="Instrumentos",
        attrs={
            "th": {"class": "table-header text-center fw-bold"},
            "td": {"class": "text-center"},
        },
    )

    class Meta:
        model = Tipo
        template_name = "django_tables2/bootstrap5.html"
        fields = ("tipo",)
        attrs = {"class": "table table-striped table-hover"}
        order_by = ("tipo",)


class EspeciesTable(tables.Table):
    favorito = tables.TemplateColumn(
        template_name="includes/agregar_favorito_column.html",
        empty_values=(),
        orderable=False,
        verbose_name="",
        attrs={
            "th": {"class": "table-header text-center text-nowrap text-small"},
            "td": {"class": "text-center text-small icon-td"},
        },
    )

    especie = tables.Column(
        verbose_name="Especie",
        empty_values=(),
        orderable=True,
        order_by=("especie",),
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-small"},
        },
    )
    plazo = tables.Column(
        verbose_name="Plazo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-center text-small"},
        },
    )
    punta_compra = tables.Column(
        verbose_name="Compra",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    punta_venta = tables.Column(
        verbose_name="Venta",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    apertura = tables.Column(
        verbose_name="Apertura",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    cierre_ant = tables.Column(
        verbose_name="Cierre ant.",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    ultimo = tables.Column(
        verbose_name="Último",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end fw-semibold text-small"},
        },
    )
    var = tables.Column(
        verbose_name="Var %",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end fw-semibold text-small"},
        },
    )
    maximo = tables.Column(
        verbose_name="Máximo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    minimo = tables.Column(
        verbose_name="Mínimo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    volumen = tables.Column(
        verbose_name="Volumen",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    monto = tables.Column(
        verbose_name="Monto Op.",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-small"},
        },
    )
    hora = tables.Column(
        verbose_name="Hora",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-center text-small"},
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
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_apertura(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_cierre_ant(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_punta_compra(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_punta_venta(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_maximo(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_minimo(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_volumen(self, value):
        formatted_value = babel.numbers.format_number(value, locale="es_AR")
        return formatted_value

    def render_monto(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
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
        attrs = {
            "class": "table table-striped table-hover table-sm",
            "id": "especiesTable",
        }
        empty_text = "No se encontraron especies"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclude = ("id",)


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

    especie = CharFilter(
        lookup_expr="icontains",
        label="Especie",
    )

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
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-nowrap text-small"},
        },
    )
    nombre = tables.Column(
        verbose_name="Nombre",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-end text-nowrap text-small truncate"},
        },
    )
    ultimo = tables.Column(
        verbose_name="Último",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-end fw-semibold text-nowrap text-small"},
        },
    )
    var = tables.Column(
        verbose_name="Var %",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-end fw-semibold text-nowrap text-small"},
        },
    )
    hora = tables.Column(
        verbose_name="Hora",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )

    def render_nombre(self, value):
        tooltip = value
        return format_html('<span title="{}">{}</span>', tooltip, value)


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
        formatted_value = babel.numbers.format_currency(
            value, "USD", "#,##0.00", locale="es_AR"
        )
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
        attrs = {
            "class": "table table-striped table-hover table-sm",
            "id": "especiesUsaTable",
        }
        empty_text = "No se encontraron especies"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclude = ("id",)


class ComparadorTable(tables.Table):
    ticker_ars = tables.Column(
        verbose_name="Ticker ARS",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-nowrap text-small"},
        },
    )
    ratio = tables.Column(
        verbose_name="Ratio",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )
    precio_ars = tables.Column(
        verbose_name="ARS",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )
    precio_ars_mep = tables.Column(
        verbose_name="ARS / MEP",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )
    precio_ars_mep_convertido = tables.Column(
        verbose_name="(ARS / MEP) * R",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-nowrap text-small"},
        },
    )
    ticker_mep = tables.Column(
        verbose_name="Ticker MEP",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )
    precio_mep = tables.Column(
        verbose_name="MEP",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )
    precio_mep_convertido = tables.Column(
        verbose_name="MEP * R",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-nowrap text-small"},
        },
    )
    ticker_usa = tables.Column(
        verbose_name="Ticker USA",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )
    precio_usa = tables.Column(
        verbose_name="USA",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-nowrap text-small"},
        },
    )
    ars_vs_usa = tables.Column(
        verbose_name="ARS/MEP vs USA",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-nowrap text-small"},
        },
    )
    mep_vs_usa = tables.Column(
        verbose_name="MEP vs USA",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center fw-semibold text-nowrap text-small"},
        },
    )
    monto_operado = tables.Column(
        verbose_name="Monto op. en mill",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center fw-bold text-small"},
            "td": {"class": "text-center text-nowrap text-small"},
        },
    )

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-sm table-striped table-hover"}
        fields = (
            "ticker_ars",
            "ratio",
            "precio_ars",
            "precio_ars_mep",
            "precio_ars_mep_convertido",
            "ticker_mep",
            "precio_mep",
            "precio_mep_convertido",
            "ticker_usa",
            "precio_usa",
            "ars_vs_usa",
            "mep_vs_usa",
            "monto_operado",
        )
        order_by = ("-monto_operado",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exclude = ("id",)


    def render_ratio(self, value):
        formatted_value = babel.numbers.format_number(value, locale="es_AR")
        return formatted_value

    def render_precio_ars(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_precio_ars_mep(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "USD", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_precio_ars_mep_convertido(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "USD", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_precio_mep(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "USD", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_precio_mep_convertido(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "USD", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_precio_usa(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "USD", "#,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_ars_vs_usa(self, value):
        if value is not None:
            value_with_percent = f"{value:.2f}%"
            color = self.color_scale(value)

            return mark_safe(
                f'<span style="color: {color};">{value_with_percent}</span>'
            )

        return value_with_percent

    def render_mep_vs_usa(self, value):
        return self.render_ars_vs_usa(value)

    def render_monto_operado(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "#,##0.00", locale="es_AR"
        )
        return formatted_value
    
    def color_scale(self, value):
        green = (0, 220, 0)
        red = (255, 0, 0)
        limit = 10

        if value is not None:
            # Normalizar el valor para que esté entre 0 y 1
            normalized_value = min(max((value + limit) / (2 * limit), 0), 1)

            r = int(green[0] + normalized_value * (red[0] - green[0]))
            g = int(green[1] + normalized_value * (red[1] - green[1]))
            b = int(green[2] + normalized_value * (red[2] - green[2]))

            return f"rgb({r},{g},{b})"

        return value

