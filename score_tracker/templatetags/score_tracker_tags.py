from django import template

register = template.Library()

@register.filter
def get_field_by_name(form, field_name):
    """
    Returns a form field with the given name.
    Usage: {{ form|get_field_by_name:"field_name" }}
    """
    try:
        return form[field_name]
    except:
        return None

@register.filter
def add(value, arg):
    """
    Adds the arg to the value.
    Usage: {{ value|add:"arg" }}
    """
    try:
        return str(value) + str(arg)
    except (ValueError, TypeError):
        return value