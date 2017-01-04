from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from datetime import datetime

from decimal import Decimal
from django.utils import timezone


import time
from django.core.exceptions import ValidationError




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
    doctortelno = models.CharField(blank=False, max_length=30) 
    illness = models.CharField(blank=False, max_length=700)

class Enterpay(models.Model):
    telno = models.CharField(blank=False, max_length=20)
    amount = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
    added = models.DateTimeField(default=datetime.now, blank=True)


class Illness(models.Model):
    added = models.DateTimeField(default=timezone.now, blank=True)
    email = models.CharField(blank=False, max_length=40)
    pname = models.CharField(blank=False, max_length=50)
    sname = models.CharField(blank=False, max_length=50)
    gender = models.CharField(blank=False, max_length=30)
    illness = models.CharField(blank=False, max_length=700)
    kin = models.CharField(blank=False, max_length=30)
    kintelno = models.CharField(blank=False, max_length=20)
    username = models.CharField(blank=False, max_length=20)
    page = models.IntegerField(blank=False)
    amb =  models.CharField(blank=False,max_length=5,  default=False)
    amt = models.CharField(blank=False,max_length=5,  default=False)
    doctortelno = models.CharField(blank=False, max_length=20)
    
   
   
class Register(models.Model):

	# user = models.OneToOneField(User)
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
    


   
class Contact(Register):

	# user = models.OneToOneField(User)
	msg = models.CharField(blank=False, max_length=20,  default=False)
	
   
class Patientr(models.Model):
    username = models.CharField(blank=False, max_length=20, unique=True)
    pwd = models.CharField(blank=False, max_length=30, unique=True)
    
class Conddrugs(models.Model):
    cond = models.CharField(blank=False, max_length=20, unique=True)
    drugs = models.CharField(blank=False, max_length=400)
    
    
class converse(models.Model):
	telno = models.CharField(blank=True, max_length=20)
	phonedoctor = models.CharField(blank=True, max_length=20)
	dmsg = models.CharField(blank=True, max_length=700)
	pmsg = models.CharField(blank=True, max_length=700)
	illness = models.CharField(blank=True, max_length=700)


class convMembers(models.Model):
	mem_phone = models.CharField(blank=True, max_length=20)
	phonedoctor = models.CharField(blank=True, max_length=20)