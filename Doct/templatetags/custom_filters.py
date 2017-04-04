'''custom filters'''
from django.template import Library
from datetime import datetime
from django.contrib.humanize.templatetags.humanize import intcomma
from decimal import Decimal
from django.utils.datastructures import SortedDict
from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorDict
from Doct.utils import CURRENCIES
from django.contrib.sites.models import Site
import random
from django.core import serializers
from Doct.utils import debug
import json
register = Library()


@register.simple_tag
def landing_background_image():
    img = random.choice(['index4.png',
     'index.png', 
     'index6.png']
     )
    return img

@register.filter
def nice_errors(form, non_field_msg='General form errors'):
    this_nice_errors = ErrorDict()
    if isinstance(form, forms.BaseForm):
        for field, errors in form.errors.items():
            if field == NON_FIELD_ERRORS:
                key = non_field_msg
            else:
                key = form.fields[field].label
            this_nice_errors[key] = errors
    return this_nice_errors


@register.filter
def get_range(value):
    str = value.split(',')
    start = int(str[0])
    end = int(str[1])
    return range(start, end)


@register.filter
def is_false(arg):
    return arg is False


@register.filter
def date_today(arg):
    return datetime.today().strftime("%B %d, %Y")


@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty * unit_price

@register.filter
def default_exchange_rate(country):
    '''
    extend this to format to default currency
    '''
    return get_default_exchange_rate(country)


def get_recipient_currency(country):
    '''
    extend this to format to default currency
    '''
    to_curr = 'UGX'
    try:
        to_curr = CURRENCIES[country]
    except Exception, e:
        pass
    return to_curr

@register.filter
def recipient_currency(country):
    '''
    extend this to format to default currency
    '''
    to_curr = 'UGX'
    try:
        to_curr = CURRENCIES[country]
    except Exception, e:
        pass
    return to_curr

def get_default_exchange_rate(country, from_curr='usd'):
    '''
    extend this to format to default currency
    '''
    value = 0
    rates = False
    to_curr = 'UGX'
    try:
        rates = Site.objects.get_current().rate
        #admin_mail(request, 'rates_error', {'error_message':repr(e)})
    except Exception, e:
        # admin_mail(request,'rates_error',{'error_message':e})
        print e
    try:
        to_curr = CURRENCIES[country]
    except Exception, e:
        pass
    if rates:
        value = rates.get_default_rate(from_curr, to_curr)
    value = round(int(value),0)
    return value

@register.filter
def default_exchange_rate_formated(country):
    '''
    extend this to format to default currency
    '''
    to_curr = 'ugx'
    try:
        to_curr = CURRENCIES[country]
    except Exception, e:
        pass
    value = get_default_exchange_rate(country)
    return "%s %s" % (to_curr, intcomma(int(value)))

def get_total_to_recipient(value, country):
    exchange = get_default_exchange_rate(country)
    value = int(exchange) * int(value)
    return value

@register.filter
def total_to_recipient(value, country):
    '''
    extend this to format to default currency
    '''
    dollars = get_total_to_recipient(value, country)
    try:
        #dollars = Decimal(str(value))
        dollars = round(int(value),0)
    except Exception, e:
        pass
    return dollars

@register.filter
def total_to_recipient_formated(value, country):
    '''
    extend this to format to default currency
    '''
    dollars = get_total_to_recipient(value, country)
    try:
        #dollars = Decimal(str(value))
        dollars = round(int(dollars),0)
    except Exception, e:
        pass
    return "%s %s" % (get_recipient_currency(country), intcomma(int(dollars)))


@register.filter
def recipient_amount_formated(value):
    '''
    extend this to format to default currency
    '''
    dollars = value
    try:
        dollars = round(int(dollars), 0)
    except Exception, e:
        pass

    try:
        dollars = intcomma(int(dollars))
    except Exception, e:
        pass
    return "UGX %s" % dollars


@register.filter
def currency(value):
    '''
    extend this to format to default currency
    '''
    dollars = 0
    try:
        #dollars = Decimal(str(value))
        dollars = round(int(value),0)
    except Exception, e:
        pass
    return "%s" % (intcomma(int(dollars)))


@register.filter
def exchange(value):
    '''
    extend this to format to default currency
    '''
    dollars = 0.00
    try:
        dollars = Decimal(str(value))
    except Exception:
        pass
    return "USD %s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])

@register.filter
def btc_exchange(value):
    '''
    extend this to format to default currency
    '''
    dollars = 0.00
    try:
        dollars = Decimal(str(value))
    except Exception:
        pass
    return "UGX %s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])


@register.filter
def keyvalue(dict, key):
    value = False
    try:
        value = dict[key]
    except Exception, e:
        pass
    return value


@register.filter(name='sort')
def listsort(value):
    if isinstance(value, dict):
        new_dict = SortedDict()
        key_list = value.keys()
        key_list.sort()
        for key in key_list:
            new_dict[key] = value[key]
        return new_dict
    elif isinstance(value, list):
        new_list = list(value)
        new_list.sort()
        return new_list
    else:
        return value
    listsort.is_safe = True


# check admin pages
@register.filter
def check_admin(request):
    return request


@register.filter
def mobile_network_code(number):
    from remit.utils import get_mobile_network_code
    return get_mobile_network_code(number)


@register.filter
def filter_response(response):
    '''filter visa and mobile response for display'''
    response = response.replace('{','')
    response = response.replace('}','')
    response = response.replace(', ',' <br /><br />')
    response = response.replace("u'","'")
    response = "<pre>%s</pre>" % response
    return response


@register.filter
def serialize_rate(obj):
    '''serialize the rate object'''
    data = {}
    try:
        serialized_obj = serializers.serialize('json', [obj, ])
        struct = json.loads(serialized_obj)
        
        try:
            del struct[0]['pk']
            del struct[0]['model']
            del struct[0]['fields']['user']
            del struct[0]['fields']['country']
            del struct[0]['fields']['added']
            del struct[0]['__proto__']
        except Exception, e:
            pass
            #debug(e, 'Error cleaning rates for javascript', 'admin')
        


        struct[0].update({'extra_fees': obj.extra_fees})
        struct[0].update({'currency': obj.country.currency})
        data = json.dumps(struct[0])
    except Exception, e:
        debug(e, 'Error serializing rates', 'admin')
    return data
