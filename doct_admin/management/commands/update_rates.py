'''management command to update currencies'''
from django.core.management.base import NoArgsCommand
from time import time
import datetime
import urllib2
from remit.models import Charge

RUN_TIME_SECONDS = 60


class Command(NoArgsCommand):

    '''management command'''
    help = """Update our currencies. Fetch\
     the currencies using cryptocharts API\
    """

    def handle_noargs(self, **options):
        #last_check_time = None
        print "starting currency update",  datetime.datetime.now()
        rates = Charge.objects.all()
        for rate in rates:
            currency = rate.country.currency
            rate.to_usd = self.convert(rate, from_curr='USD', to_curr=currency)
            rate.to_eur = self.convert(rate, from_curr='EUR', to_curr=currency)
            rate.to_gbp = self.convert(rate, from_curr='GBP', to_curr=currency)
            rate.to_kes = self.convert(rate, from_curr='KES', to_curr=currency)
            rate.to_rwf = self.convert(rate, from_curr='RWF', to_curr=currency)
            rate.to_ugx = self.convert(rate, from_curr='UGX', to_curr=currency)
            rate.to_tzs = self.convert(rate, from_curr='TZS', to_curr=currency)
            rate.save()
        print "finished currency update", datetime.datetime.now()

    def get_data(self, from_curr, to_curr):
        url = 'http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=%s%s=X' % (
            from_curr, to_curr)
        #url = self.URL.format(from_curr=from_curr, to_curr=to_curr)
        request = urllib2.Request(url, None, {'Accept-encoding': '*'})
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError:
            return None
        result = response.read()
        return result

    def convert(self, rate, from_curr, to_curr='USD', amount=1.00):
        '''convert the currency'''
        if from_curr.lower() == to_curr.lower():
            return amount
        data = self.get_data(from_curr, to_curr)
        if data:
            exchange = data.split(',')
            try:
                if len(exchange[1]) > 1:
                    default = u'{0:.3f}'.format(
                        round(float(exchange[1]) * amount, 3))
                else:
                    default = rate.get_default_rate(to_curr)
            except (IndexError, ValueError):
                default = rate.get_default_rate(to_curr)
            default = float(default) - \
                self.percentage(rate.forex_percentage, default)
        return default

    def percentage(self, percent, whole):
        '''get the percentage of'''
        new_percent = (float(percent) * float(whole)) / 100.0
        return new_percent
