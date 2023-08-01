import django_tables2 as tables
from django.utils import timezone
from django.utils.safestring import mark_safe
from .models import Operacion
from django.urls import reverse

import locale, pytz
import babel.numbers
from decimal import Decimal

class TenenciaTable(tables.Table):
    tipo = tables.Column(
        verbose_name="Tipo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap columna-tabla-tenencia"},
            "td": {"class": "text-start text-nowrap fw-medium"},
        },
    )

    activo = tables.Column(
        verbose_name="Activo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap columna-tabla-tenencia"},
            "td": {"class": "text-start text-nowrap fw-medium"},
        },
    )

    cantidad = tables.Column(
        verbose_name="Cantidad",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-tenencia"},
            "td": {"class": "text-end text-nowrap fw-medium"},
        },
        footer="Total:",
    )

    tenencia_ars = tables.Column(
        verbose_name="Ten. ARS",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-tenencia"},
            "td": {"class": "text-end text-nowrap fw-semibold"},
        },
        #footer=lambda table: locale.currency(
        #    sum(x["tenencia_ars"] for x in table.data), symbol="", grouping=True
        #),
        footer=lambda table: babel.numbers.format_currency(
            sum(Decimal(x["tenencia_ars"]) for x in table.data),
            currency="$",
            format=u'#,##0.00',
            locale='es_AR',
        ),
    )

    tenencia_usd = tables.Column(
        order_by=("tenencia_usd",),
        verbose_name="Ten. USD",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-tenencia"},
            "td": {"class": "text-end text-nowrap fw-semibold"},
        },
        #footer=lambda table: locale.currency(
        #    sum(x["tenencia_usd"] for x in table.data), symbol="", grouping=True
        #),
        footer=lambda table: babel.numbers.format_currency(
            sum(Decimal(x["tenencia_usd"]) for x in table.data),
            currency="USD",
            format=u'#,##0.00',
            locale='es_AR',
        ),

    )

    def render_cantidad(self, value):
        #locale.setlocale(locale.LC_ALL, "es_AR")
        #formatted_value = locale.format_string("%.0f", value, grouping=True)
        formatted_value = babel.numbers.format_number(value, locale='es_AR')
        return formatted_value

    def render_tenencia_ars(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.2f", value, grouping=True)
            formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')

            if value < 0:
                return mark_safe(f'<span style="color: red;">{formatted_value}</span>')
            elif value > 0:
                return mark_safe(
                    f'<span style="color: forestgreen;">{formatted_value}</span>'
                )
        return formatted_value

    def render_tenencia_usd(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.2f", value, grouping=True)
            formatted_value = babel.numbers.format_currency(value, 'USD', u'#,##0.00', locale='es_AR')

            if value < 0:
                return mark_safe(f'<span style="color: red;">{formatted_value}</span>')
            elif value > 0:
                return mark_safe(
                    f'<span style="color: forestgreen;">{formatted_value}</span>'
                )
        return formatted_value

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-sm table-responsive-lg"}
        fields = ("tipo", "activo", "cantidad", "tenencia_ars", "tenencia_usd")
        order_by = ("-tenencia_usd",)


class ResultadosTable(tables.Table):
    #locale.setlocale(locale.LC_ALL, "es_AR.utf8")
    tipo = tables.Column(
        verbose_name="Tipo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start"},
            "td": {"class": "text-start fw-medium"},
        },
    )

    activo = tables.Column(
        verbose_name="Activo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start columna-tabla-resultado"},
            "td": {"class": "text-start fw-medium"},
        },
    )

    cantidad = tables.Column(
        verbose_name="En tenencia",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end columna-tabla-resultado"},
            "td": {"class": "text-end fw-medium"},
        },
        footer="Total:",
    )

    resultado_ars = tables.Column(
        verbose_name="Resultado ARS",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end columna-tabla-resultado"},
            "td": {"class": "text-end fw-semibold"},
        },
        #footer=lambda table: locale.currency(
        #    sum(x["resultado_ars"] for x in table.data), symbol="", grouping=True
        #),
        footer=lambda table: babel.numbers.format_currency(
            sum(Decimal(x["resultado_ars"]) for x in table.data),
            currency="$",
            format=u'#,##0.00',
            locale='es_AR',
        ),
    )

    resultado_usd = tables.Column(
        order_by=("resultado_usd",),
        verbose_name="Resultado USD",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end columna-tabla-resultado"},
            "td": {"class": "text-end fw-semibold"},
        },
        #footer=lambda table: locale.currency(
        #    sum(x["resultado_usd"] for x in table.data), symbol="", grouping=True
        #),
        footer=lambda table: babel.numbers.format_currency(
            sum(Decimal(x["resultado_usd"]) for x in table.data),
            currency="USD",
            format=u'#,##0.00',
            locale='es_AR',
        ),
    )

    def render_cantidad(self, value):
        #locale.setlocale(locale.LC_ALL, "es_AR")
        #formatted_value = locale.format_string("%.0f", value, grouping=True)
        formatted_value = babel.numbers.format_number(value, locale='es_AR')
        return formatted_value

    def render_resultado_ars(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.2f", value, grouping=True)
            formatted_value = babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')
            
            if value < 0:
                return mark_safe(f'<span style="color: red;">{formatted_value}</span>')
            elif value > 0:
                return mark_safe(
                    f'<span style="color: forestgreen;">{formatted_value}</span>'
                )
        return formatted_value

    def render_resultado_usd(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.2f", value, grouping=True)
            formatted_value = babel.numbers.format_currency(value, 'USD', u'#,##0.00', locale='es_AR')

            if value < 0:
                return mark_safe(f'<span style="color: red;">{formatted_value}</span>')
            elif value > 0:
                return mark_safe(
                    f'<span style="color: forestgreen;">{formatted_value}</span>'
                )
        return formatted_value

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-sm"}
        fields = ("tipo", "activo", "cantidad", "resultado_ars", "resultado_usd")
        order_by = ("-resultado_usd",)


class OperacionesTable(tables.Table):
    tipo = tables.Column(
        verbose_name="Tipo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap"},
            "td": {"class": "text-start text-nowrap"},
        },
    )

    plazo = tables.Column(
        verbose_name="Plazo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap"},
            "td": {"class": "text-start text-nowrap"},
        },
    )

    activo = tables.Column(
        verbose_name="Activo",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-start text-nowrap"},
        },
    )

    especie = tables.Column(
        verbose_name="Especie",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-start text-nowrap"},
        },
    )

    fecha = tables.Column(
        verbose_name="Fecha",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-start text-nowrap"},
        },
    )

    cotiz_mep = tables.Column(
        verbose_name="Cotiz. MEP",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap  columna-tabla-operaciones"},
            "td": {"class": "text-center text-nowrap"},
        },
    )

    operacion = tables.Column(
        verbose_name="Operación",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-center text-nowrap"},
        },
    )

    cantidad = tables.Column(
        verbose_name="Cantidad",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-end text-nowrap"},
        },
    )

    precio_ars = tables.Column(
        verbose_name="Precio ARS",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-end text-nowrap"},
        },
    )

    precio_usd = tables.Column(
        verbose_name="Precio USD",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-end text-nowrap"},
        },
    )

    total_ars = tables.Column(
        verbose_name="Total ARS",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-end text-nowrap"},
        },
    )

    total_usd = tables.Column(
        verbose_name="Total USD",
        empty_values=(),
        orderable=True,
        attrs={
            "th": {"class": "table-header text-end text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-end text-nowrap"},
        },
    )

    editar = tables.TemplateColumn(
        template_name="includes/editar_operacion_column.html",
        orderable=False,
        verbose_name="Editar",
        attrs={
            "th": {"class": "table-header text-center text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-center text-nowrap"},
        },
    )

    eliminar = tables.TemplateColumn(
        template_name="includes/eliminar_operacion_column.html", empty_values=(),
        orderable=False,
        verbose_name="Eliminar",
        attrs={
            "th": {"class": "table-header text-center text-nowrap columna-tabla-operaciones"},
            "td": {"class": "text-center text-nowrap"},
        },
    )

    def render_especie(self, value):
        especie_str = value.especie
        return especie_str.split(" ")[0]

    def render_fecha(self, value):
        local_timezone = pytz.timezone(
            "Greenwich"
        )  # Replace 'Your_Timezone' with your desired timezone
        localized_datetime = timezone.localtime(value, local_timezone)
        formatted_datetime = localized_datetime.strftime("%d-%m-%Y %H:%M")
        return formatted_datetime

    def render_cotiz_mep(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.2f", value, grouping=True)
            formatted_value = babel.numbers.format_currency(value, '$', u'¤¤ #,##0.00', locale='es_AR')
        return formatted_value

    def render_cantidad(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.0f", value, grouping=True)
            formatted_value = babel.numbers.format_number(value, locale='es_AR')
        return formatted_value

    def render_precio_ars(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.2f", value, grouping=True)
            formatted_value = babel.numbers.format_currency(value, '$', u'¤¤ #,##0.00', locale='es_AR')
        return formatted_value

    def render_precio_usd(self, value):
        if value is not None:
            #locale.setlocale(locale.LC_ALL, "es_AR")
            #formatted_value = locale.format_string("%.2f", value, grouping=True)
            formatted_value = babel.numbers.format_currency(value, 'USD', u'¤¤ #,##0.00', locale='es_AR')
        return formatted_value
    
    def render_total_ars(self, record):
        if record is not None:
            formatted_value = babel.numbers.format_currency(record.calculate_total_ars(), '$', u'¤¤ #,##0.00', locale='es_AR')
        return formatted_value
    
    def render_total_usd(self, record):
        if record is not None:
            formatted_value = babel.numbers.format_currency(record.calculate_total_usd(), 'USD', u'¤¤ #,##0.00', locale='es_AR')
        return formatted_value

    class Meta:
        model = Operacion
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-sm"}
        fields = (
            "tipo",
            "plazo",
            "activo",
            "especie",
            "fecha",
            "cotiz_mep",
            "operacion",
            "cantidad",
            "precio_ars",
            "precio_usd",
            "total_ars",
            "total_usd",
        )
        order_by = ("-fecha",)
