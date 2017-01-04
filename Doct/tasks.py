from __future__ import unicode_literals

from djsms import send_text
from django.core.mail import EmailMultiAlternatives
from Doct.models import settings


frm = '+33123456789'
to = '+33987654321'
text = 'Please remember to pick up the bread before coming'
send_text(text, frm, to)


def send_email(subject,  msg, sender, to):
    """schedule email sending."""
    if settings.DISABLE_COMMS:
        return True
    msg = EmailMultiAlternatives(subject, msg, sender, to)

    print "sent mail from %s to %s" % (sender, to)
    return msg.send()

