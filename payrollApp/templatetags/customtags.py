from django import template

register = template.Library()

@register.filter(name='getID')
def getID(value):
  return int(value.split("|")[0])