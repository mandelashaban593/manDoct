''' generate summary reports and send to admin'''
from remit.models import Transaction
from datetime import datetime,  timedelta
from django.shortcuts import HttpResponse


def get_ipay_commission(successful_transactions):
    commission = 0 
    for transaction in successful_transactions:
        commission += (3.2 * float(transaction.amount_sent + transaction.our_charge)) / float(100.0)
    return commission


def summary_reports(daily=False):
    ''' generate summary reports and send to admin'''
    response = {}    
    start_date = datetime.today()
    if daily:
        start_date = start_date - timedelta(days=1)
        transactions = Transaction.objects.filter(processed_on__contains=start_date.date())
    else:
        end_date = start_date - timedelta(days=7)
        transactions = Transaction.objects.filter(started_on__range=(start_date, end_date))


    if transactions:
        from django.db.models import Sum
        total_transactions = transactions.count()
        successful_transactions = transactions.filter(
            visa_success=True, is_processed=True, amount_sent__isnull=False)
        pending_transactions = transactions.filter(
            visa_success=True, is_processed=False, amount_sent__isnull=False)

        total_transactions_usd = successful_transactions.aggregate(Sum('amount_sent'))
        total_transactions_usd = total_transactions_usd['amount_sent__sum']

        
        pending_transactions_count = pending_transactions.count()
        delivered_transactions = successful_transactions.count()
        
        delivered_amount = successful_transactions.aggregate(Sum('amount_received'))
        delivered_amount = delivered_amount['amount_received__sum']

        pending_amount = pending_transactions.aggregate(Sum('amount_received'))
        pending_amount = pending_amount['amount_received__sum']


        transfer_fees = (5.4 * float(total_transactions_usd)) / float(100.0)
        ipay_commission = get_ipay_commission(successful_transactions)#(3.2 * float(delivered_amount)) / float(100.0) #100 * float(delivered_amount)/3.2
        bank_fee = 30
        
        

        yo_commission = (0.5 * float(delivered_amount)) / float(100.0)
        forex = (3.5 * float(delivered_amount)) / float(100.0)

        if not daily:
            to_bank = float(total_transactions_usd) + float(transfer_fees) - ipay_commission - 30
       
        import csv
        import StringIO
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        csvfile = StringIO.StringIO()
        writer = csv.writer(csvfile)
        
        header = [
            smart_str(u"Total Transactions (count) "),
            smart_str(u"Total Transactions (amount) "),
            smart_str(u"Transfer fees"),
            smart_str(u"Ipay Commission"),
            smart_str(u"Bank Fee"),
            smart_str(u"Delivered Transactions"),
            smart_str(u"Delivered Amount"),
            smart_str(u"Pending Transactions"),
            smart_str(u"Pending Amount"),
            smart_str(u"Yo Commission"),
            smart_str(u"Forex"),
        ]

        content = [
            smart_str(total_transactions),
            smart_str(total_transactions_usd),
            smart_str(transfer_fees),
            smart_str(ipay_commission),
            smart_str(bank_fee),
            smart_str(delivered_transactions),
            smart_str(delivered_amount),
            smart_str(pending_transactions_count),
            smart_str(pending_amount),
            smart_str(yo_commission),
            smart_str(forex),
        ]

        if not daily:
            header.append( smart_str(u"Bank Fee"),)
            content.append( smart_str(to_bank),)

        writer.writerow(header)
        writer.writerow(content)

        date = start_date.strftime("%B-%d-%Y")

        from django.core.mail import EmailMultiAlternatives    
        subject = 'Daily Transaction report for %s' % date
        if not daily:
            subject = 'Weekly Transaction report from %s to %s' % ( start_date.strftime("%B-%d-%Y"),
             end_date.strftime("%B-%d-%Y"))
        msg = EmailMultiAlternatives(subject, subject, 
            'admin@remit.ug', ['atwine@gmail.com'])
        msg.attach('report_%s.csv' % date, 
            csvfile.getvalue(), 'text/csv')
        return msg.send()
    return False
