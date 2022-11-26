import datetime
from django import template

register = template.Library()

@register.filter(name='my_filter_name')
def my_filter_name(input):
    # output 
    # return output
    return 'output'

register.filter('my_filter_name', my_filter_name)