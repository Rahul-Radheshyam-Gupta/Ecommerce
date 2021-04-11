from django import template
import json
from datetime import datetime
register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary:
      return dictionary.get(key)
    else:
      return None

@register.filter
def mulplication(a,b):
  try:
    return a*b
  except :
    return 0

