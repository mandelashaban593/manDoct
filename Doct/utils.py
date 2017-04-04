from manDoct.settings import *
from django.contrib import messages
from django.shortcuts import render_to_response, render, \
    get_object_or_404, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext


CURRENCIES = {
    'KE': 'KES',
    'UG': 'UGX',
    'RW': 'RWF'
}

COUNTRY_CODE = {
    'KE': 254,
    'UG': 256,
    'RW': 250
}

NETWORK_CHOICES = (
    ('MTN', 'MTN Mobile Money'),
    ('AIRTEL', 'Airtel Money'),
    ('UTL', 'M-Sente'),
)


COUNTRY_CHOICES = (
    ('UG', 'Uganda'),
    ('KE', 'Kenya'),
    ('TZ', 'Tanzania'),
    ('RW', 'Rwanda'),
)



def check_illness(post_values):
    from rango.models import Illness
    '''check if a number exists in a phonebook'''
    try:
        check_illness = Illness.objects.get(
            email=post_values['email'],
            pname=post_values['pname'],
            # firstname=post_values['firstname'],
            # lastname=post_values['lastname'],
            gender=post_values['gender'],
            illness=post_values['illness'],
            kin=post_values['kin'],
            kintelno=post_values['kintelno'],
            username=post_values['username'],
            page=post_values['page'],
        )
        return check_illness
    except Exception, e:
        return False


def check_diognosis(post_values):
    from rango.models import Diognosis
    '''check if a number exists in a phonebook'''
    try:
        check_illness = Illness.objects.get(
            dname=post_values['dname'],
            telno=post_values['telno'],
            # firstname=post_values['firstname'],
            # lastname=post_values['lastname'],
            gender=post_values['gender'],
            diognosis=post_values['diognosis'],
            payi=post_values['payi'],
            email=post_values['email'],
        )
        return check_illness
    except Exception, e:
        return False       


        dname = request.POST['dname']
#       telno = request.POST['telno']
#       gender = request.POST['gender']
#       diognosis = request.POST['diognosis']
#       page = request.POST['page']
#       payi = request.POST['payi']
#       email = request.POST['email']

def mailer(request, subject, msg, to, sender=False):
    if settings.DISABLE_COMMS:
        return True
    if not sender:
        sender = settings.APP_EMAILS['info']
    
    #send_email(subject, msg, sender, to)
    


    
        
    return True



def success_message(request, msgtype, data={}):
    template = settings.BASE_DIR + 'templates/Doct/success_messages.html'
    data['type'] = msgtype
    text = render_to_string(
        template, data, context_instance=RequestContext(request))
    messages.success(request, text)


def error_message(request, msgtype, data={}):
    template = settings.BASE_DIR + 'templates/Doct/error_messages.html'
    data['type'] = msgtype
    text = render_to_string(
        template, data, context_instance=RequestContext(request))
    messages.error(request, text)