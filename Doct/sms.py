from  manDoct.settings import *
from django.template.loader import render_to_string








def send_illness_sms_notification(message, to):
    from twilio.rest import TwilioRestClient
    response = False
    to = '+256754307471'
    
    client = TwilioRestClient(
        settings.TWI_ACCOUNT_SID, settings.TWI_AUTH_TOKEN)
    response = client.messages.create(
        body=message, to=to, from_='+16092574786')
    try:
        debug(e, 'Twi sms response %s' % response, 'sms')
    except Exception, e:
        pass
    return response
