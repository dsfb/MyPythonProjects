from django import template

register = template.Library()

@register.filter
def return_list(value, arg):
    return [i for i in range(int(arg))]
