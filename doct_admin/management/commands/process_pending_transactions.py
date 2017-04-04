'''process pending Transactions'''
from django.core.management.base import NoArgsCommand
from remit.models import Transaction
from datetime import datetime
from django.contrib.auth.models import User
from payments import payment


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
        pending_transactions = Transaction.momo.pending()
        if len(pending_transactions) > 0:
            print "Started processing %s Pending Transactions %s" % (
                len(pending_transactions),
                datetime.now()
                )
            user = User.objects.get(pk=1)
            for transaction in pending_transactions:
                response = {}
                response = payment.process_mobilemoney(
                        transaction, response, request=False, processed_by=user)
                print response
        print "Finished processing Pending Transactions %s" % datetime.now()