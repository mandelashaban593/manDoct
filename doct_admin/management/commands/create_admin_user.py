'''management command to update currencies'''
from django.core.management.base import NoArgsCommand
from time import time
import datetime
from remit_admin.views import generate_csv_report, get_country_access, get_network_access
from remit.models import Transaction
from accounts.models import AdminProfile
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User


class Command(NoArgsCommand):

    '''management command'''
    help = """Send Customer Service Reports\
           """

    def handle_noargs(self, **options):
        start_time = time()
        start_date = datetime.datetime.now()
        end_date = start_date = datetime.datetime.now()
        print "start create admin user ", time() - start_time
        self.send_report(
            country_code='UG',
            mobile_network="MTN",
            start_date=start_date,
            end_date=end_date,
        )
        print "end create admin user", datetime.datetime.now()
