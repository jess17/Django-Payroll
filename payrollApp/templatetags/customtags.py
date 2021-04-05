from django import template

register = template.Library()

@register.filter(name='getID')
def getID(value):
  if value != str('None'):
    return int(value.split("|")[0])
  else:
    return 'None'

# @register.filter(name='getName')
# def getName(value):
#   return str(value.split("|")[1])