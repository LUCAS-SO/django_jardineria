from django import template

register = template.Library()

@register.filter
def duration(value):
    """
    Convierte minutos → 'Xh Ym'
    """
    if value is None:
        return ""

    try:
        value = int(value)
    except:
        return value

    hours = value // 60
    minutes = value % 60

    if hours > 0 and minutes > 0:
        return f"{hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{minutes}m"
