'''management command to update currencies'''
from django.core.management.base import NoArgsCommand
from time import time
import datetime
from summary_reports import summary_reports

    
RUN_TIME_SECONDS = 60


class Command(NoArgsCommand):

    '''management command'''
    help = """Update our currencies. Fetch\
     the currencies using cryptocharts API\
    """

    def handle_noargs(self, **options):
        start_time = time()
        #last_check_time = None
        print "generating daily report", time() - start_time
        summary_reports(daily=False)
        print "sent daily report on", datetime.datetime.now()
