from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from datetime import datetime

from decimal import Decimal
from django.utils import timezone

from django.contrib.sites.models import Site
import time
from django.core.exceptions import ValidationError

from Doct.utils import NETWORK_CHOICES
from Doct.utils import COUNTRY_CHOICES
from django.contrib.auth.models import Permission
import urllib
import hashlib
from django.utils.translation import ugettext as _
from django.contrib.admin.models import LogEntry



class Page(models.Model):
	title=models.CharField(max_length=128)
	url=models.URLField()
	views=models.IntegerField(default=0)


	def __unicode__(self):
		return self.title



class  UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	# Override the __unicode__() method to return out something meaningful !
	def __unicode__(self):
		return self.user.username




class Topup(models.Model):

	
	amount_sent = models.CharField("Airtime", max_length=50)
	receiver_number = models.CharField(max_length=50, blank=False)
	receiver_fname= models.CharField(max_length=100, blank=False)
	receiver_lname= models.CharField(max_length=100, blank=False)
	sender_fullname = models.CharField(max_length=100)
	receiver_country_code = models.CharField(max_length=200)
	added = models.DateTimeField()
	productcode= models.CharField(max_length=100, blank=False)
	comments= models.CharField(max_length=100, blank=False)
	

	def __str__(self):
		return "%s %s %s %s %s" % (self.amount_sent,self.receiver_number , self.receiver_fname ,self.receiver_country_code , self.added )







# Doctor consult Websit models




class Diognosis(models.Model):
    dname = models.CharField(blank=False, max_length=40)
    telno = models.CharField(blank=False, max_length=20)
    gender = models.CharField(blank=False, max_length=30) # This is the payment Id
    diognosis = models.CharField(blank=False, max_length=700)
    added = models.DateTimeField(default=timezone.now, blank=True)
    page = models.IntegerField(blank=False)
    email = models.CharField(blank=False,max_length=50,  default=False)
    amb =  models.CharField(blank=False,max_length=5,  default=False)
    is_prescribed = models.BooleanField(default=False)
    compill =  models.CharField(blank=False, max_length=700)
    fup =  models.CharField(blank=False, max_length=700)
    reply =  models.CharField(blank=False, max_length=700)
    amt = models.CharField(blank=False, max_length=30) 
    doctorusername = models.CharField(blank=False, max_length=30) 
    illness = models.CharField(blank=False, max_length=700)
    comp_signs =  models.CharField(blank=False, max_length=700) 
    ill_id  =  models.CharField(blank=False, max_length=30)
    username = models.CharField(blank=False, max_length=20)
    when  =  models.DateTimeField(default=datetime.now, blank=True)
    dtelno = models.CharField(blank=False, max_length=20)

    @models.permalink
    def edit_diognosis(self):
        return ('Doct/editdiog', ({self.pk}), {})


class Enterpay(models.Model):
    telno = models.CharField(blank=False, max_length=20)
    amount = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
    added = models.DateTimeField(default=datetime.now, blank=True)
    dname = models.CharField(blank=False, max_length=40)


class Illness(models.Model):
    added = models.DateTimeField(default=timezone.now, blank=True)
    email = models.CharField(blank=False, max_length=40)
    pname = models.CharField(blank=False, max_length=50)
    sname = models.CharField(blank=False, max_length=50)
    gender = models.CharField(blank=False, max_length=30) # gender is the payment Id
    illness = models.CharField(blank=False, max_length=700)  
    comp_signs =  models.CharField(blank=False, max_length=700) 
    kin = models.CharField(blank=False, max_length=30)
    kintelno = models.CharField(blank=False, max_length=20)
    username = models.CharField(blank=False, max_length=20)
    page = models.IntegerField(blank=False)
    amb =  models.CharField(blank=False,max_length=5,  default=False)
    amt = models.CharField(blank=False,max_length=5,  default=False)
    doctorusername = models.CharField(blank=False, max_length=20)
    location = models.CharField(blank=False, max_length=700)
    when  =  models.DateTimeField(default=datetime.now, blank=True)
    dtelno = models.CharField(blank=False, max_length=20)
    dname = models.CharField(blank=False, max_length=40)

    def get_names(self):
        '''
        Return a users phonenumber
        '''
        text = '%s %s' % (self.pname, self.sname)
        try:
            text = text.encode('utf-8')
        except UnicodeEncodeError:
            pass
        return text
    
   
   

    

    
    

   

	
   
class Patientr(models.Model):
    username = models.CharField(blank=False, max_length=20, unique=True)
    pwd = models.CharField(blank=False, max_length=30, unique=True)
    
class Conddrugs(models.Model):
    cond = models.CharField(blank=False, max_length=20, unique=True)
    drugs = models.CharField(blank=False, max_length=400)
    
    
class converse(models.Model):
	username = models.CharField(blank=True, max_length=20)
	dusername  = models.CharField(blank=True, max_length=20)
	dmsg = models.CharField(blank=True, max_length=700)
	pmsg = models.CharField(blank=True, max_length=700)
	illness = models.CharField(blank=True, max_length=700)


class convMembers(models.Model):
	mem_username = models.CharField(blank=True, max_length=20)
	dusername  = models.CharField(blank=True, max_length=20)


class convReg(models.Model):
	mem_username  = models.CharField(blank=True, max_length=20)
	names= models.CharField(blank=True, max_length=300, default=False)





class Messages(models.Model):
	password_phone = models.CharField(blank=True, max_length=20)
	msg = models.CharField(blank=True, max_length=700)
	password_phone = models.CharField(blank=True, max_length=20)
	




class convPersonFrien(models.Model):
	person_password = models.CharField(max_length=30)
	friend_password = models.CharField(max_length=30)
 
	
	
# chating app






class Country(models.Model):
    code = models.CharField(blank=False, max_length=4, unique=True)
    name = models.CharField(blank=False, max_length=40)
    currency = models.CharField(blank=False, max_length=4, unique=True)
    user = models.ForeignKey(User)
    added = models.DateTimeField(default=datetime.now, blank=True)
    dailing_code = models.CharField(blank=False, max_length=5, default=256)

    @models.permalink
    def admin_charges_limits_url(self):
        return ('admin:admin_charges_limits', (str(self.code),),)

    @models.permalink
    def admin_rates_limits_url(self):
        return ('admin:admin_rates', (str(self.code),),)

    @property
    def rates(self):
        charge = Charge.objects.get(country=self.pk)
        return charge

    


class Charge(models.Model):
    '''currency and exchange rates for each country'''
    country = models.ForeignKey(Country, null=True, blank=True)
    forex_percentage = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    transfer_fee_percentage = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    transfer_maximum_usd = models.DecimalField(
        default=500.00, decimal_places=2, max_digits=10)
    transfer_minimum_usd = models.DecimalField(
        default=100.00, decimal_places=2, max_digits=10)
    mtn_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    airtel_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    orange_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    tigo_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    safaricom_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    vodafone_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    general_network_charge = models.DecimalField(
        default=60.00, decimal_places=2, max_digits=10)
    user = models.ForeignKey(User)
    added = models.DateTimeField(default=datetime.now, blank=True)
    to_usd = models.DecimalField(
        default=2640.00, decimal_places=2, max_digits=10)
    to_gbp = models.DecimalField(
        default=3974.00, decimal_places=2, max_digits=10)
    to_eur = models.DecimalField(
        default=3256.00, decimal_places=2, max_digits=10)
    to_rwf = models.DecimalField(
        default=1114.76, decimal_places=2, max_digits=10)
    to_ugx = models.DecimalField(
        default=2640.00, decimal_places=2, max_digits=10)
    to_kes = models.DecimalField(
        default=85.63, decimal_places=2, max_digits=10)
    to_tzs = models.DecimalField(
        default=1623.00, decimal_places=2, max_digits=10)

    @property
    def last_update(self):
        epoch = int(time.mktime(self.added.timetuple()) * 1000)
        return epoch

    @property
    def currency(self):
        '''currency'''
        return str(self.country.currency)

    @property
    def hashid(self):
        '''
        invoice number
        '''
        return str(self.pk ^ 0xABCDEFAB)

    def get_default_rate(self, to_curr):
        '''return default rate , defaults to usd-ugx'''
        curr = 2500.00
        to_curr = to_curr.lower()
        if to_curr == 'usd':
            curr = self.to_usd
        if to_curr == 'gbp':
            curr = self.to_gbp
        if to_curr == 'eur':
            curr = self.to_eur
        return curr

    @property
    def extra_fees(self):
        '''extra network fees'''
        extra_fees = {}
        exts = country_extensions(self.country.code)
        this_charge = 0
        for key, value in exts.iteritems():
            if key == 'airtel':
                this_charge = self.airtel_charge
            elif key == 'safaricom':
                this_charge = self.safaricom_charge
            elif key == 'mtn':
                this_charge = self.mtn_charge
            elif key == 'tigo':
                this_charge = self.tigo_charge
            for x in value:
                extra_fees.update({x: '%s' % this_charge})
        return extra_fees

    def save(self, *args, **kwargs):
         # check if the charge already exists
        if not self.pk:
            if not Charge.objects.filter(country=self.country).exists():
                # continue with save, if necessary:
                super(Charge, self).save(*args, **kwargs)
            else:
                return
        else:
            super(Charge, self).save(*args, **kwargs)




def current_percentage():
    '''current website percentage , backwards compatability , using Charge now'''
    return False


class Transaction(models.Model):

    '''remit Transactions'''
    

    class Meta:
        permissions = (
            ('view_transaction', 'View Transactions'),
            ('edit_transaction', 'Edit Transactions'),
            ('view_reports', 'View Reports'),
        )

    user = models.ForeignKey(User, related_name="owner")
    # rate defaults to current site rate
    exchange_rate = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
    currency_sent = models.CharField(default='UGX', max_length=3)
    currency_received = models.CharField(default='USD', max_length=3)
    amount_sent = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=10)
    amount_received = models.DecimalField(
        null=False, blank=False, decimal_places=2, max_digits=10)
    receiver_number = models.CharField(blank=False, max_length=130)
    receiver_country_code = models.CharField(default='256', max_length=3)
    receiver_fname = models.CharField(
        blank=True, max_length=30, default=False)
    receiver_lname = models.CharField(
        blank=True, max_length=30, default=False)
    started_on = models.DateTimeField(blank=False, default=timezone.now)
    added = models.DateTimeField(default=timezone.now)

    our_charge = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=100)
    our_percentage = models.DecimalField(
        default=current_percentage, decimal_places=2, max_digits=10)
    total_charge = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
    other_fees = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)

    visa_response_time = models.DateTimeField(null=True, blank=True)
    visa_response_code = models.CharField(
        blank=True, max_length=30, default=False)
    visa_response_metadata = models.TextField(blank=True, default=False)
    visa_success = models.BooleanField(default=False)
    visa_processed = models.BooleanField(default=False)

    mobile_money_success = models.BooleanField(default=False)

    mobile_response_time = models.DateTimeField(null=True, blank=True)
    mobile_response_code = models.CharField(
        blank=True, max_length=30, default=False)
    mobile_response_metadata = models.TextField(blank=True, default=False)
    mobile_reason = models.CharField(blank=True, max_length=220, default=False)

    is_processed = models.BooleanField(default=False)
    marked_as_processed = models.BooleanField(default=False)
    processed_on = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        User, null=True, blank=True, related_name="admin_processed")
    updated_by = models.ForeignKey(
        User, null=True, blank=True, related_name="admin_update_by")
    to_country = models.ForeignKey(
        Country, related_name="target_country", null=True, blank=True)
    mobile_network_code = models.CharField(
        blank=True, max_length=100, choices=NETWORK_CHOICES, default=False)
    sender_country = models.CharField(blank=True, max_length=30)
    utility = models.BooleanField(default=False)
    wallet = models.BooleanField(default=False)
    referencenumber = models.CharField(
        blank=True, default=False, max_length=230
    )
    billtype = models.CharField(blank=True, default=False, max_length=230)
    billarea = models.CharField(blank=True, default=False, max_length=230)
    utility_account_name = models.CharField(
        blank=True, default=False, max_length=230)
    utility_account_type = models.CharField(
        blank=True, default=False, max_length=230)
    is_canceled = models.BooleanField(default=False)
    canceled_reason = models.CharField(
        blank=True, default=False, max_length=230)
    canceled_by = models.ForeignKey(
        User, null=True, blank=True, related_name="admin_canceled")
    canceled_on = models.DateTimeField(null=True, blank=True)
   


    @property
    def last_pk(self):
        t = Transaction.objects.all().order_by('-id')[:1][0]
        return t.pk

    def get_network_transactionid(self):
        return "%s" % self.mobile_response_code

    def get_mobile_network(self):
        '''retuns mobile mobile'''
        number = '%s' % self.receiver_number
        return get_mobile_network_code(number)

    def revenue_share(self):
        from manDoct.settings import REVENUE_SHARE
        shs = 0
        if self.is_processed:
            try:
                percent = REVENUE_SHARE
                whole = float(self.amount_received)
                shs = (percent * whole) / 100.0
                shs = float(shs)
            except Exception, e:
                print e
        return shs

    @property
    def successful(self):
        '''
        filter successful Transactions
        '''
        result = False
        if self.visa_success and self.is_processed and self.amount_sent:
            result = True
        return result

    @property
    def mobile_successful(self):
        """filter mobile successfuel transactions."""
        result = False

        if self.mobile_money_success and self.is_processed and self.amount_sent:
            result = True

        return result

    @property
    def hashid(self):
        '''
        invoice number
        '''
        return str(self.pk ^ 0xABCDEFAB)

    def get_invoice(self):
        '''
        invoice number
        '''
        return str(self.pk ^ 0xABCDEFAB)

    def get_sender_profile(self):
        from Doct.models import Profile
        '''
        sender profile
        '''
        return Profile.objects.get(user=self.user.pk)

    def get_order_id(self):
        '''
        invoice number
        '''
        return str(self.pk ^ 0xABCDEFAB)

    def recipient_number(self):
        '''
        number of person receiving the funds
        '''
        number = '%s%s' % (self.receiver_country_code, self.receiver_number)
        return str(number)

    def paybill_recipient_number(self):
        '''
        number of person receiving the funds
        '''
        number = '%s%s' % (self.receiver_country_code, self.receiver_number)
        return str(number)

    @property
    def actual_amount_received(self):
        '''get actual amount sent'''
        ugx_amount = self.amount_received
        try:
            if self.other_fees:
                other_fees = float(self.other_fees)
                amount_received = float(ugx_amount)
                ugx_amount = amount_received - other_fees
        except Exception, e:
            print e
        try:
            ugx_amount = round(ugx_amount, 2)
        except Exception, e:
            print e
        return ugx_amount

    @property
    def other_fees_local(self):
        '''get other fees charged'''
        return self.other_fees

    @models.permalink
    def admin_url(self):
        '''return admin url link'''
        # print self.uid
        return ('admin:admin_transaction', ({self.get_invoice()}), {})

    @models.permalink
    def get_receipt_url(self):
        '''return admin url link'''
        # print self.uid
        return ('admin:transaction_receipt', ({self.get_invoice()}), {})

    @property
    def actual_initiation_date(self):
        from pytz import timezone
        try:
            return self.started_on.astimezone(timezone('Africa/Nairobi')).strftime("%d-%m-%Y %I:%M %p")
        except Exception, e:
            pass

    @property
    def actual_status(self):
        status = 'Failed'
        if self.is_processed:
            status = 'Processed'
        elif self.visa_success == True and self.is_processed == False and self.amount_sent is not None:
            status = 'Pending'
        return status

    @property
    def actual_delivery_date(self):
        from pytz import timezone
        try:
            return self.processed_on.astimezone(timezone('Africa/Nairobi')).strftime("%d-%m-%Y %I:%M %p")
        except Exception, e:
            pass

    def is_pending(self):
        pending = False
        if self.visa_success == True and self.is_processed == False and self.amount_sent is not None:
            pending = True
        return pending

    def mobile_is_pending(self):
        pending = False

        if self.mobile_money_success and not self.is_processed and self.amount_sent is not None:
            pending = True
        return pending

    def processed_by_profile(self):
        from Doct.models import Profile
        profile = False
        try:
            profile = Profile.objects.get(user=self.processed_by.pk)
        except Exception, e:
            pass
        return profile

    def visa_response_data(self):
        from payments.payment import RESPONSE_CODES
        data = self.visa_response_code
        if data == RESPONSE_CODES['SUCCESS'] or self.visa_success:
            data = "Card Charged Successfully"
        else:
            data = "Failure Charging Card"

        if not data or data == 'False':
            data = 'N/A'
        return data

    def mobile_money_response_data(self):
        """mobile money filter."""
        #data = self.
        if self.mobile_money_success:
            data = "Successful"
        else:
            data = "Failed"

        if not data or data == 'False':
            data = "N/A"
        return data


    def mobile_response_data(self):
        data = False
        data = self.mobile_response_metadata
        try:
            if 'statusmessage' in data:
                data = data['statusmessage']
        except Exception, e:
            pass
        if not data or data == 'False':
            data = 'N/A'
        return data

    def recipient_names(self):
        '''
        name of person receiving the funds
        '''
        name = '%s %s' % (self.receiver_fname, self.receiver_lname)
        return str(name)

    def sender_number(self):
        '''
        number of person sending the funds
        '''
        from Doct.models import Profile
        profile = Profile.objects.get(user=self.user)
        return "%s" % profile.get_phonenumber()

    def sender_names(self):
        '''
        number of person sending the funds
        '''
        from Doct.models import Profile
        profile = Profile.objects.get(user=self.user.pk)
        return "%s" % profile.get_names()

    def sender_reason(self):
        '''
        mobile money reason
        '''
        #from remit.settings import BASE_URL
        mobile_reason = self.mobile_reason
        if not mobile_reason or mobile_reason == 'False':
            #mobile_reason = "Mobile Money from %s via %s" % (self.sender_names(), BASE_URL)
            mobile_reason = "Mobile Money from %s" % self.sender_names()
        return mobile_reason

    def recipient_country(self):
        countries = {'256': 'UGANDA', '254': 'KENYA',
                     '255': 'TANZANIA', '250': 'RWANDA'}
        country = "UGANDA"
        try:
            country = str(countries[str(self.receiver_country_code)])
        except Exception, e:
            print e
        return country

    def display_amount_received(self):
        dollars = self.actual_amount_received
        currency = 'UGX'
        try:
            dollars = float(round(dollars, 2))
            currency = self.to_country.currency
        except Exception, e:
            pass
        return "%s %s" % (currency, intcomma(int(dollars)))

    def display_exchange_rate(self, amount=1):
        '''get the rate'''
        rate = Site.objects.get_current().rate
        code = int(self.receiver_country_code)
        dollars = rate.usd_to_ugx
        if code == 254:
            dollars = rate.usd_to_kes
        try:
            dollars = round(int(dollars), 0)
        except Exception, e:
            pass
        return "USD %s = %s %s" % (amount, self.to_country.currency, intcomma(int(dollars)))

    def get_extra_fees(self, number, rate):
        # other charges
        other_fees = False
        try:
            number = str(number)
            ext = number[:2]
            other_fees = rate.extra_fees[ext]
            other_fees = Decimal(str(other_fees))
        except Exception, e:
            debug(e, 'Error getting other fees', 'Transaction')
        return other_fees

    def save(self, *args, **kwargs):
        add = not self.pk
        #super(Transaction, self).save(*args, **kwargs)
        if add:

            # get Charge object
            profile = self.get_sender_profile()
            rate = profile.current_rate()

            try:
                self.amount_sent = Decimal(str(self.amount_sent))
                self.amount_sent = Money(amount_sent)
            except Exception, e:
                pass

            # current exchange rate
            self.exchange_rate = rate.to_usd

            amount_sent = self.amount_sent

            # our charge
            our_charge = rate.transfer_fee_percentage % amount_sent
            self.our_charge = Decimal(str(our_charge))

            # total charge
            total_charge = our_charge + amount_sent
            self.total_charge = Decimal(str(total_charge))

            self.to_country = rate.country

            # add the network
            number = '%s' % self.receiver_number
            self.mobile_network_code = get_mobile_network_code(number)

            r_amount = amount_sent * self.exchange_rate
            self.amount_received = r_amount

            self.other_fees = self.get_extra_fees(number, rate)

            if profile.country:
                self.sender_country = profile.country
            else:
                self.sender_country = 'UGANDA'
            # create() uses this, which causes error.
            kwargs['force_insert'] = False

            # Fast forward Pk Values
            try:
                from manDoct.settings import FORCE_TRANSACTION_ID
                if FORCE_TRANSACTION_ID:

                    self.pk = self.last_pk + 1
                    
                    super(Transaction, self).save(*args, **kwargs)
            except Exception, e:
                print "Failed Forcing ID %s" % e
        super(Transaction, self).save(*args, **kwargs)
        return self




class Profile(models.Model):

    '''user profile information'''

    class Meta:
        permissions = (
            ('view_profile', 'View Profiles'),
            ('edit_profile', 'Edit Profiles'),
        )

    '''Profile for normal user'''
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    email_activation_key = models.CharField(_('activation key'),
                                            max_length=40,
                                            blank=True)
    phone_activation_key = models.CharField(_('phone activation'),
                                            max_length=4,
                                            blank=True)
    firstname = models.CharField(blank=True, max_length=50)
    lastname = models.CharField(blank=True, max_length=50)
    email_activated = models.BooleanField(default=False)
    userdetails_provided = models.BooleanField(default=False)
    id_verified = models.BooleanField(default=False)
    id_scanned = models.BooleanField(default=False)
    id_scan_ref = models.CharField(blank=True, max_length=50)
    id_verify_ref = models.CharField(blank=True, max_length=50)
    account_blocked = models.BooleanField(default=False)
    account_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    country_code = models.CharField(blank=True, default=False, max_length=10)
    phonenumber = models.CharField(blank=True, default=False, max_length=20)
    address1 = models.TextField(blank=True, default=False)
    address2 = models.TextField(blank=True, default=False)
    dob = models.DateTimeField(null=True, blank=True)
    country = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=30)
    id_number = models.CharField(blank=True, max_length=30)

    #id_pic = models.ImageField(upload_to=path_and_rename("images/uploads/"), blank=True)
    id_pic = models.ImageField(upload_to="img/uploads/", blank=True)

    id_type = models.CharField(blank=True, max_length=30)
    id_expiry = models.CharField(blank=True, max_length=30)
    joined = models.DateTimeField(default=datetime.now)
    blocked_by = models.ForeignKey(
        User, null=True, blank=True, related_name="admin_blocked")
    verified_by = models.ForeignKey(
        User, null=True, blank=True, related_name="admin_verified")
    verification_attempts = models.IntegerField(default=0)
    unverified_by = models.ForeignKey(
        User, null=True, blank=True, related_name="admin_unverified")
    unblocked_by = models.ForeignKey(
        User, null=True, blank=True, related_name="admin_unblocked")
    status_updated_on = models.DateTimeField(null=True, blank=True)

    # profile_pic = models.ImageField(
    #    upload_to=path_and_rename("images/images/thumbs/"), blank=True)
    profile_pic = models.ImageField(upload_to="img/images/thumbs/",
                                    blank=True
                                    )
    #is_bitcoin_user = models.BooleanField(default=False)

    # profile_pic = models.ImageField(
    #    upload_to=profile_path_and_rename, null=True, blank=True)
    send_country_code = models.CharField(
        blank=False, default='256', max_length=10)

    # get the current rate for the user
    def current_rate(self):
        '''get the curent rate of the User'''
        from Doct.models import Country
        return Country.objects.get(dailing_code=self.send_country_code).rates

    def passport_extension(self):
        name, extension = os.path.splitext(self.id_pic.name)
        return extension

    def get_phonenumber(self):
        '''
        Return a users phonenumber
        '''
        return str('%s%s' % (self.country_code, self.phonenumber))

    def get_ipay_phonenumber(self):
        '''
        Return a users phonenumber for ipay form
        '''
        tel = self.get_phonenumber()
        try:
            if len(tel) < 1:
                tel = settings.CONTACT_NO
            tel = tel.replace('+', '')
        except Exception, e:
            pass
        return tel

    def get_names(self):
        '''
        Return a users phonenumber
        '''
        text = '%s %s' % (self.firstname, self.lastname)
        try:
            text = text.encode('utf-8')
        except UnicodeEncodeError:
            pass
        return text

    def user_can_sendmoney(self):
        '''
        If a user is a allowed to send money
        '''
        can_send = self.userdetails_provided
        return can_send

    @models.permalink
    def admin_url(self):
        '''return admin url link'''
        # print self.uid
        return ('admin:admin_user', ({"pk": self.uid}), {})
        #url = reverse('admin:admin_user', kwargs={self.uid})
        # return str(url)
        # return str(settings.BASE_URL + 'admin/user/%s' % (self.uid()))

    @models.permalink
    def get_unique_url(self):
        '''
        direct link to profile
        '''
        return('profile', [str(self.pk ^ 0xABCDEFAB)])

    def __unicode__(self):
        return str('%s %s' % (self.firstname, self.lastname))

    @property
    def uid(self):
        return str(self.pk ^ 0xABCDEFAB)

    @property
    def avatar(self, size="100"):
        '''gravatar image'''
        profile_pic = self.profile_pic
        if not profile_pic:
            gravatar_url = settings.GRAVATAR_URL
            gravatar_url += urllib.urlencode({
                'gravatar_id': hashlib.md5(self.user.email).hexdigest(),
                'size': str(size)
            })
        else:
            gravatar_url = profile_pic.url
        return gravatar_url





class Rate(models.Model):

    '''Rates and Transaction limits'''
    from Doct.models import Profile

    class Meta:
        permissions = (
            ('view_rate', 'View Rates'),
            ('edit_rate', 'Edit Rates'),
        )

    '''fetch rates and store them'''
    site = models.OneToOneField(Site, default=1)
    usd_to_rwf = models.DecimalField(
        default=688.00, decimal_places=2, max_digits=10)
    gbp_to_rwf = models.DecimalField(
        default=1114.76, decimal_places=2, max_digits=10)
    usd_to_ugx = models.DecimalField(
        default=2640.00, decimal_places=2, max_digits=10)
    usd_to_kes = models.DecimalField(
        default=85.63, decimal_places=2, max_digits=10)
    usd_to_tzs = models.DecimalField(
        default=1623.00, decimal_places=2, max_digits=10)
    gbp_to_ugx = models.DecimalField(
        default=3974.19, decimal_places=2, max_digits=10)
    gpb_to_kes = models.DecimalField(
        default=129.47, decimal_places=2, max_digits=10)
    gpb_to_tzs = models.DecimalField(
        default=2453.00, decimal_places=2, max_digits=10)
    transfer_limit_usd = models.DecimalField(
        default=500.00, decimal_places=2, max_digits=10)
    transfer_minimum_usd = models.DecimalField(
        default=100.00, decimal_places=2, max_digits=10)
    bill_transfer_minimum_ugx = models.DecimalField(
        default=5000.00, decimal_places=2, max_digits=10)
    our_percentage = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    percentage_from_forex = models.DecimalField(
        default=4.50, decimal_places=2, max_digits=10)
    user = models.ForeignKey(User)
    added = models.DateTimeField(default=datetime.now, blank=True)

    def get_rate(self, amount, rate=usd_to_ugx):
        return amount * self[rate]

    def currency_to_usd(self):
        'return the default currency amount in ugx'
        return self.usd_to_ugx

    def currency_transfer_maximum(self):
        'return the default currency amount transfer limit defaults to usd'
        return self.transfer_limit_usd

    def currency_transfer_minimum(self):
        'return the default currency amount transfer limit defaults to usd'
        return self.transfer_minimum_usd

    def remit_charge(self):
        'return the remit chagre defaults to our percentage'
        return self.our_percentage

    def kenyan_fees(self):
        '''temp value for kenyan fees'''
        # return 60
        return 0

    def get_default_rate(self, from_curr, to_curr):
        '''return default rate , defaults to usd-ugx'''
        curr = 2500.00
        from_curr = from_curr.lower()
        to_curr = to_curr.lower()
        if from_curr == 'usd':
            if to_curr == 'ugx':
                curr = self.usd_to_ugx
            if to_curr == 'tzs':
                curr = self.usd_to_tzs
            if to_curr == 'kes':
                curr = self.usd_to_kes
        return curr

    def last_modified_by(self):
        return self.user.username

    @property
    def airtel_charge(self):
        return 300

    @property
    def mtn_charge(self):
        '''temp value'''
        return 390
        # return 0


def current_percentage():
    '''current website percentage , backwards compatability , using Charge now'''
    return False


def current_rate():
    '''current rate , backwards compatability , using charge now'''
    return False

class Register(models.Model):

    # user = models.OneToOneField(User)
    user = models.OneToOneField(User)
    fname = models.CharField(blank=True, max_length=20,  default=False)
    sname = models.CharField(blank=True, max_length=30,  default=False)
    page = models.IntegerField(blank=True)
    gender = models.CharField(blank=True, max_length=30,  default=False)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    username = models.CharField(blank=True, max_length=20,default=False)
    password= models.CharField(max_length=30)
    email = models.CharField(blank=True,max_length=50,  default=False)
    street = models.CharField(blank=True,max_length=50,  default=False)
    city = models.CharField(blank=True,max_length=20, default=False)
    state = models.CharField(blank=True,max_length=20,  default=False)
    zip_code = models.CharField(blank=True,max_length=5,  default=False)
    specialty = models.CharField(max_length=20, default=False)
    role = models.CharField(max_length=20, default=False)
    profile_pic = models.ImageField(upload_to="images/uploads/", blank=True)
    account_blocked = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_names(self):
        '''
        Return a users phonenumber
        '''
        text = '%s %s' % (self.fname, self.lname)
        try:
            text = text.encode('utf-8')
        except UnicodeEncodeError:
            pass
        return text

    def __unicode__(self):
        return self.user.username







class Contact(models.Model):

    # user = models.OneToOneField(User)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    email = models.CharField(blank=True,max_length=50,  default=False)
    msg = models.CharField(blank=False, max_length=20,  default=False)



class LoginInfo(models.Model):
    '''store login data'''
    login_time = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    remote_addr = models.IPAddressField()
    user = models.ForeignKey(User, blank=False, null=False)

    

    

class UserActions(models.Model):
    '''store user actions'''
    session = models.ForeignKey(LoginInfo, blank=False, null=False)
    log_entry = models.ForeignKey(LogEntry, blank=False, null=False)
    user = models.ForeignKey(User, blank=False, null=False)

    @property
    def user_location(self):
        location = 'UnKnown'
        try:
            if self.session.remote_addr:
                import requests
                r = requests.get('http://ipinfo.io/%s/json' %
                                 self.session.remote_addr)
                loc = r.json()
                if 'ip' in loc:
                    location = '%s' % loc['ip']
                if 'country' in loc:
                    location += ',%s' % loc['country']
                if 'city' in loc:
                    location += ',%s' % loc['city']
                if 'region' in loc:
                    location += ',%s' % loc['region']
        except Exception, e:
            pass
        return location




class Ambulance(models.Model):
    '''store login data'''
    amb_time = models.DateTimeField(auto_now_add=True)
    districts = models.CharField(max_length=1000, blank=True, null=True)
    place = models.CharField(blank=True, max_length=100,  default=False)
    phone = models.CharField(blank=True, max_length=20,  default=False)







class Orderdrugs(models.Model):

    # user = models.OneToOneField(User)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    location = models.CharField(blank=True,max_length=50,  default=False)
    msg = models.CharField(blank=False, max_length=20,  default=False)
    when = models.DateTimeField(auto_now_add=True)


class Labtests(models.Model):

    # user = models.OneToOneField(User)
    telno = models.CharField(blank=True, max_length=20,  default=False)
    location = models.CharField(blank=True,max_length=500,  default=False)
    msg = models.CharField(blank=False, max_length=20,  default=False)
    when = models.DateTimeField(auto_now_add=True)