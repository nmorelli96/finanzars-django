from django.utils.safestring import mark_safe
import django_tables2 as tables
from datetime import datetime
import babel.numbers

class FiatTable(tables.Table):
    dolar = tables.Column(
        verbose_name="",
        orderable=False,
        attrs={
            "th": {"class": "table-header text-start fiat-hora-header"},
            "td": {"class": "text-nowrap"},
        },
    )
    compra = tables.Column(
        orderable=False,
        attrs={
            "th": {"class": "table-header text-center"},
            "td": {"class": "text-nowrap text-center"},
        },
    )
    venta = tables.Column(
        orderable=False,
        attrs={
            "th": {"class": "table-header text-center"},
            "td": {"class": "text-nowrap text-center"},
        },
    )
    var = tables.Column(
        verbose_name="Var %",
        orderable=False,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-nowrap text-center"},
        },
    )

    class Meta:
        template_name = "django_tables2/bootstrap5.html"
        attrs = {"class": "table table-sm table-striped table-hover"}

    def render_compra(self, value):
        if isinstance(value, float):
            formatted_value = babel.numbers.format_currency(
                value, "$", "#,##0.00", locale="es_AR"
            )
            return formatted_value
        else:
            return value

    def render_venta(self, value):
        if isinstance(value, float):
            formatted_value = babel.numbers.format_currency(
                value, "$", "#,##0.00", locale="es_AR"
            )
            return formatted_value
        else:
            return value
        
    def render_var(self, value):
        if value is not None:
            if isinstance(value, float) and value != 0:
                absolute_value = abs(value)
                value_with_percent = f"{absolute_value:.2f}%"
            else:
                return '—'
            if value < 0:
                return mark_safe(
                    f'<span style="color: crimson;">{value_with_percent}▼</span>'
                )
            elif value > 0:
                return mark_safe(
                    f'<span style="color: forestgreen;">{value_with_percent}▲</span>'
                )
        return value_with_percent


class BancosTable(tables.Table):
    banco = tables.Column(
        verbose_name="Entidad",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap"},
            "td": {"class": "text-start text-nowrap"},
        },
    )
    compra = tables.Column(
        verbose_name="Compra",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )
    venta = tables.Column(
        verbose_name="Venta",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )
    ventaTot = tables.Column(
        verbose_name="V+100%",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )
    hora = tables.Column(
        verbose_name="Hora",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )

    def render_compra(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "¤¤ #,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_venta(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "¤¤ #,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_ventaTot(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "¤¤ #,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_hora(self, value, record):
        timestamp = datetime.fromtimestamp(value)
        formatted_value = timestamp.strftime("%H:%M")  # Formato de hora deseado
        time_diff = (datetime.now() - timestamp).total_seconds()
        full_date_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        color = "red" if time_diff > 3600 else "green"
        return mark_safe(
            f'<span title="{full_date_time}" <span style="color: {color};">{formatted_value}</span>'
        )

    class Meta:
        attrs = {"class": "table table-sm table-striped table-hover"}
        template_name = "django_tables2/bootstrap5.html"
        order_by = ("ventaTot",)


class CryptosTable(tables.Table):
    banco = tables.Column(
        verbose_name="Exchange",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-start text-nowrap"},
            "td": {"class": "text-start text-nowrap"},
        },
    )
    coin = tables.Column(
        verbose_name="Coin",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )
    compra = tables.Column(
        verbose_name="Compra",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )
    venta = tables.Column(
        verbose_name="Venta",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )
    hora = tables.Column(
        verbose_name="Hora",
        orderable=True,
        attrs={
            "th": {"class": "table-header text-center text-nowrap"},
            "td": {"class": "text-center text-nowrap"},
        },
    )

    def render_compra(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "¤¤ #,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_venta(self, value):
        formatted_value = babel.numbers.format_currency(
            value, "$", "¤¤ #,##0.00", locale="es_AR"
        )
        return formatted_value

    def render_hora(self, value, record):
        timestamp = datetime.fromtimestamp(value)
        formatted_value = timestamp.strftime("%H:%M")
        time_diff = (datetime.now() - timestamp).total_seconds()
        full_date_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        color = "red" if time_diff > 3600 else "green"
        return mark_safe(
            f'<span title="{full_date_time}" <span style="color: {color};">{formatted_value}</span>'
        )

    class Meta:
        attrs = {"class": "table table-sm table-striped table-hover"}
        template_name = "django_tables2/bootstrap5.html"
        order_by = ("venta",)
