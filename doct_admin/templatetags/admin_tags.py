''' admin tags '''
from django import template
from django.template.loader import render_to_string, TemplateDoesNotExist
from remit_admin.utils import  LOG_ACTION
register = template.Library()


@register.filter
def action_type(value):
	try:
		mydict = LOG_ACTION
		return mydict.keys()[mydict.values().index(value)]
	except Exception, e:
		print e
	