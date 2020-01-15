from django import template

register = template.Library()


@register.simple_tag
def get_cat(fdict, key, val):
    if  fdict.get(key) == val:
        return 'selected'
    else:
        return ''

