'''management command to update currencies'''
from django.core.management.base import NoArgsCommand
from time import time
import datetime
from remit_admin.views import generate_csv_report, get_country_access, get_network_access 
from remit.models import Transaction
from accounts.models import AdminProfile
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives


class Command(NoArgsCommand):

    '''management command'''
    help = """Send Customer Service Reports\
           """

    def handle_noargs(self, **options):
        start_time = time()
        start_date = datetime.datetime.now()
        end_date = start_date = datetime.datetime.now()
        print "sending daily Customer Service report", time() - start_time
        self.send_report(
            country_code='UG', 
            mobile_network="MTN",
            start_date=start_date, 
            end_date=end_date,
            )
        print "sent Customer Service report on", datetime.datetime.now()

    def send_report(self, country_code, mobile_network, start_date, end_date):
        # restrict a user
        try:
            admin = AdminProfile.objects.filter(
                mobile_network=mobile_network,
                country=country_code
                )[:1]
            if len(admin) > 0:
                admin = admin[0] 
                csvfile = generate_csv_report(
                self.transaction_list(
                    country_code,
                    mobile_network,
                    start_date, 
                    end_date
                    ),
                user=admin.user,
                _file=True,
                )
                '''mail the report'''
                date = start_date.strftime("%B-%d-%Y")
                subject = 'Daily Transaction report for %s' % date
                
                lst = self.mail_list(mobile_network_code='MTN')
                for email in lst:
                    msg = EmailMultiAlternatives(subject, subject, 'admin@remit.ug', ['%s' % email])
                    msg.attach('report_%s.csv' % date, 
                        csvfile.getvalue(), 'text/csv')
                    msg.send()
        except AdminProfile.DoesNotExist:
            print "Admin Profile not found"
        except Exception, e:
            print "Exception occured %s" % e


    def transaction_list(self, country_code, mobile_network, start_date, end_date):
        '''
        transaction list
        '''
        transactions = Transaction.objects.filter(
                visa_success=True,
                to_country__code=country_code,
                amount_sent__isnull=False,
                mobile_network_code=mobile_network
                )
        if transactions:
            transactions = transactions.filter(
                 Q(started_on__range=(start_date, end_date)) 
                 | Q(started_on__startswith=start_date.date()) 
                 | Q(started_on__startswith=end_date.date())
                )
        return transactions


    def mail_list(self, mobile_network_code):
        lst = {}
        if mobile_network_code =='MTN':
            lst = {'madra@199fix.com'}
        return lst