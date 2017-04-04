'''process pending Transactions'''
from django.core.management.base import NoArgsCommand
from remit.models import Transaction
from datetime import datetime
from django.contrib.auth.models import User
from payments import payment
import json
import re

class Command(NoArgsCommand):

    '''management command'''
    help = """Update our currencies. Fetch\
     the currencies using cryptocharts API\
    """

    def handle_noargs(self, **options):
        """
        pending_transactions = Transaction.objects.filter(
            visa_success=True, is_processed=False, amount_sent__isnull=False)
        """
        pending_transactions = Transaction.billpayments.pending()
        if len(pending_transactions) > 0:
            print "Started processing utility %s Pending Transactions %s" % (
                len(pending_transactions),
                datetime.now()
                )
            user = User.objects.get(pk=1)
            for transaction in pending_transactions:
                response = {}
                vendorid = None
                try:
                    response = transaction.mobile_response_metadata
                    j = re.sub(r"{\s*(\w)", r'{"\1', response)
                    j = re.sub(r",\s*(\w)", r',"\1', j)
                    j = re.sub(r"(\w):", r'\1":', j)
                    response = json.dumps(j)
                    response = json.loads(response)
                    print response
                    result = response['result']
                    print result
                    vendorid = result.get('vendor_transaction_id')
                except Exception, e:
                    print e
                print vendorid
                #print response
        print "Finished processing Pending Transactions %s" % datetime.now()