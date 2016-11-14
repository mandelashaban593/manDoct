from __future__ import unicode_literals

from djsms import send_text


frm = '+33123456789'
to = '+33987654321'
text = 'Please remember to pick up the bread before coming'
send_text(text, frm, to)