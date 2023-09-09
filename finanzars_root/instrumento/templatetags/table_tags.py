from django import template
import babel.numbers
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def format_currency(value):
    return babel.numbers.format_currency(value, '$', u'#,##0.00', locale='es_AR')

@register.filter
def format_percentage(value):
    return babel.numbers.format_percent(value, u'#,##0.00%', locale='es_AR')

@register.filter
def var_color(value):
    try:
        # Intenta convertir el valor a un número en punto flotante
        value = float(value.replace(',', '.')) if isinstance(value, str) else float(value)
        
        if value < 0:
            return mark_safe(f'<span style="color: red;">{value}%▼</span>')
        elif value > 0:
            return mark_safe(f'<span style="color: forestgreen;">{value}%▲</span>')
        else:
            return mark_safe(f'<span style="color: grey;">{value}%</span>')
    except (ValueError, TypeError):
        print(ValueError)
        return mark_safe(f'<span>{value}%</span>')
