# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, render

from Doct.decorators import ajax_required, login_required
from django.http import HttpResponse

from Doct.models import Page, UserProfile, Topup,Register, Enterpay,Illness, Diognosis,Conddrugs,Contact,converse,convMembers,convReg,convPersonFrien,Messages,Labtests

from Doct.forms import  UserForm,DiognosisForm
from Doct.forms import PageForm, TopupForm, PatientForm, IllnessForm,DoctorForm,AddIllDetForm,ContactForm, LoginForm,patientConverseForm,doctorConverseForm, MessagesForm,UserProfileForm
from django.contrib.auth.models import  User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from  manDoct.settings import *
from django.template.loader import render_to_string
from Doct.utils import check_illness,mailer,success_message, error_message
from Doct.sms import send_illness_sms_notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from Doct.models import Transaction, Rate, Country, Charge,Ambulance,Orderdrugs
from Doct.utils import COUNTRY_CHOICES, NETWORK_CHOICES

# Create your views here.
from django.shortcuts import HttpResponse, render_to_response, \
    HttpResponseRedirect, render
from django.core.urlresolvers import reverse
from django.template import RequestContext
from Doct.models import Page,Transaction, UserProfile, Country, Topup,Register, Enterpay,Illness, Diognosis,Conddrugs,Contact,converse,convMembers,convReg,convPersonFrien,Messages
from django.contrib import messages

import doct_admin.utils as admin_utils
from django.contrib.auth.models import User
from django.db.models import Sum, Max


def dashboard_stats(request):
	country = None

	r = None
	try:
		r = Register.objects.get(password=password, username=username)
	except Exception, e:
		print "Invalid Username Or Password", e
	data = {'boss_man': False}
	countries = Country.objects.all()

	profile = User.objects.filter(
        is_superuser=False, is_staff=False).count()
	data['user_count'] = profile
	data['verified_user_count'] = admin_utils.verified_users(
        count=True)
	data['blocked_user_count'] = admin_utils.blocked_users(count=True)
	data['pending_user_count'] = admin_utils.users_pending_verification(
        count=True)
	transaction = Transaction.objects.filter(
        visa_success=True, is_processed=False, amount_sent__isnull=False).aggregate(Sum('amount_sent'))
	data['amount_pending'] = transaction['amount_sent__sum']
	currency = None
	for country in countries:
		currency = country.currency.lower()


    

    
        
        # amount pending
        transaction = Transaction.objects.filter(
            visa_success=True, is_processed=False, amount_sent__isnull=False).aggregate(Sum('amount_received'))
        data['amount_pending_%s' % currency] = transaction[
            'amount_received__sum']
        # pending transactions
        transaction = Transaction.objects.filter(
            visa_success=True, is_processed=False, amount_sent__isnull=False).count()

        data['pending_transactions_%s' % currency] = transaction
        transaction = Transaction.objects.filter(visa_success=False, is_processed=False, amount_sent__isnull=False).count()
   	data['failed_transactions'] = transaction
   	transaction = Transaction.objects.filter(
        visa_success=True, is_processed=True, amount_sent__isnull=False).aggregate(Sum('amount_sent'))
   	data['total_amount_transfered'] = transaction['amount_sent__sum']
   	transaction = Transaction.objects.filter(
        visa_success=True, is_processed=True, amount_sent__isnull=False).aggregate(Sum('amount_sent'))
   	data['total_amount_transfered'] = transaction['amount_sent__sum']
   	transaction = Transaction.objects.filter(
        visa_success=True, is_processed=True, amount_sent__isnull=False).aggregate(Sum('amount_received'))
   	data['total_amount_transfered_ugx'] = transaction['amount_received__sum']
   	data['user_with_transaction'] = Transaction.objects.filter(
        visa_success=True, is_processed=True, amount_sent__isnull=False).values('user').distinct().count()
   	data['complete_transactions'] = Transaction.objects.filter(
        visa_success=True, is_processed=True, amount_sent__isnull=False).count()
   	return data
    


   
    

    
    

    
    

    
    

    
    

    
    
    


    






def index(request):

	context=RequestContext(request)

	return render_to_response('Doct/index.html', context)
	
	




def add_page(request):
	# Get the context from the request

	context=RequestContext(request)


	# A HTTP POST?
	if request.method=='POST':
		form=PageForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new page to the database.
			form.save(commit=True)


			# Now call the index() view.
			# The user will be shown the homepage.
			return index(request)
		else:
			# The supplied form contained errors- Just print them to the terminal.
			print form.errors
	else:
		# if the request was not a POST, display the form to enter details.
		form=PageForm()

	# Bad form(or form details), no form supplied...
	# Render the form with error messages (if any).
	return render_to_response('Doct/add_page.html', {'form':form}, context)


def p_reg(request):
	# Like before, get the request's context.
	context = RequestContext(request)

	registered = False
	signup = False


	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
	   	

		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = PatientForm(data=request.POST)

		# if the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()

			profile = profile_form.save()
			
			registered = True
			return render_to_response(
			'Doct/index.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'signup':signup},
			context)



		
		else:
			print user_form.errors, profile_form.errors

	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form = PatientForm()
		signup=True


# Render the template depending on the context.

	return render_to_response(
	'Doct/register.html',
	{'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'signup':signup},
	context)



def regdoctor(request):
	# Like before, get the request's context.
	context = RequestContext(request)

	registered = False

	if request.method == 'POST':
		
		user_form = UserForm(data=request.POST)
		doctreg_form = DoctorForm(data=request.POST)

		# if the two forms are valid...
		if user_form.is_valid() and doctreg_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()

	
			doctreg = doctreg_form.save()
			
			registered = True

		else:
			print user_form.errors, doctreg_form.errors


	else:
		user_form = UserForm()
		doctreg_form = DoctorForm()


# Render the template depending on the context.
	return render_to_response(
	'Doct/register1.html',
	{'user_form': user_form, 'profile_form': doctreg_form, 'registered': registered},
	context)


def  how_it_works(request):
	context = RequestContext(request)

	return render_to_response(
	'Doct/how_it_works.html',
	{},
	context)





def  send_at(request):
	context = RequestContext(request)


	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	sent_airtime = False

	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		topup_form = TopupForm(data=request.POST)
		

		# if the two forms are valid...
		if topup_form.is_valid():
			# Save the user's form data to the database.
			user = topup_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			

			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model untill we're ready to avoid integrity problems.
		
			sent_airtime = True
			# Did the user provihde a profile picture?
			# If so, we neeed to get it from the input form and put it in the  UserProfile model.
			
			# Invalid form orr forms - mistakes or something else?
			# Print problems to the terminial.
			# They'll also be shown to the user.
			# They'll also be shown top the user.
		else:
			print topup_form.errors

	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		topup_form= TopupForm()
		


# Render the template depending on the context.
	return render_to_response(
	'Doct/send_at.html',
	{'topup_form': topup_form, 'sent_airtime': sent_airtime},
	context)




def airtime_sent_details(request):
	context = RequestContext(request)

	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.

		contact = request.POST['receiver_number']
		
		contents = Topup.objects.filter(receiver_number=contact).order_by('-id')

		return render_to_response(
	'Doct/airtime_sent_details.html',
	{'contents': contents},
	context)

		
	else:

	
		

		return render_to_response('rango/trans_dform.html', {}, context)








def add_page(request, category_name_url):
	context = RequestContext(request)
	
	category_name = decode_url(category_name_url)

	if request.method == 'POST':
		form = PageForm(request.POST)
		
		if form.is_valid():

			# This time we cannot commit straight away.
# Not all fields are automatically populated!
			page = form.save(commit=False)
# Retrieve the associated Category object so we can add it.
			cat = Category.objects.get(name=category_name)
			page.category = cat
# Also, create a default value for the number of views.
			page.views = 0
# With this, we can then save our new model instance.
			page.save()
# Now that the page is saved, display the category instead.
			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm()

	return render_to_response( 'Doct/add_page.html',
	{'category_name_url': category_name_url,
	'category_name': category_name, 'form': form},
	context)






 


def user_login(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	response = None
	log = False
	convmem = ''
	phonedoctor = ''
	data = {}
	password = None
	username = None
	staf=False


	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		password = request.POST.get('password', None)
		username = request.POST['username']
		r = None	
		data.update({'admin_data': dashboard_stats(request)})

		print "Username %s "  % (username) 
		print "Password %s "  % (password)
		

	
		r = get_object_or_404(Register.objects.filter(password=password, username=username))
		

		if r:
			print "Username 1 %s "  % (username) 
			print "Password 1 %s "  % (password)
			print "Role 1 %s "  % (r.role)
			if r.role=='patient':
				patlog=True
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)

						return render_to_response('Doct/patientH.html', {'patlog':patlog}, context)
			elif r.role =='doctor':

				print "Uername 2 %s "  % (username) 
				print "Password 2 %s "  % (password)
				print "Role 2 %s "  % (r.role)

				doctlog=True
				try:
					diog = Diognosis.objects.all().order_by("-id")
					convmem = convMembers.objects.filter(mem_username=username)
				except Exception, e:
					print 'Error, retrieving diog or convmem ', e

				if convmem:
					username=username
					print username
				
				paginator = Paginator(diog, settings.PAGNATION_LIMIT2)
				page = request.GET.get('page')
				try:
					diog = paginator.page(page)
				except PageNotAnInteger:
					diog = paginator.page(1)
					# If page is not an integer, deliver first page.
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					diog = paginator.page(paginator.num_pages)

				staf=True
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						return render_to_response('Doct/index_staff.html', {'diogs':diog,'data':data ,'staf':staf, 'username':username,'doctlog':doctlog}, context)
			        			
			elif r.role =='admin':
				print "Username 3 %s "  % (username) 
				print "Password 3 %s "  % (password)
				print "Role 3 %s "  % (r.role)

				super_admin = True
				staf=True
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						
						return render_to_response('Doct/index_admin.html', {'staf':staf, 'super_admin':super_admin, 'data':data}, context)
						
			else:
				return render_to_response('Doct/index.html', {}, context)
		else:
			messages.error(request,
                                    "Incorrect username or password"
                                    )
			response = True

			 # return HttpResponse(response)
			return render_to_response('Doct/index.html', {'response':response}, context)

			 
			 

	elif request.method == 'GET':
		log = True
		return render_to_response('Doct/index.html', {'log':log}, context)
		
	
		
		

def user_log(request):
		context = RequestContext(request)
		u_log = True
		return render_to_response('Doct/login_user.html', {'u_log':u_log}, context)





def authConsult(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		telno = request.POST['telno']
		tdy = request.POST['tdy']


		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		
		p = Enterpay.objects.filter(telno=telno, added=tdy)
		


		# If we have  a User object, the details are correct.
		# if None (Python's  way of  representing the absent of a value), no user
		# with matching credentials was found.
		if p:
		
			return render_to_response('Doct/illness.html', {}, context)
		else:
				# An inactive account was used - no logging in!
			msg = "Wrong number or day"
			msg2 = "You can call us at 0754307471"
			return render_to_response('Doct/authconsult.html', {'msg':msg, 'msg2': msg2}, context)
		

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likey be a HTTP GET.
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		return render_to_response('Doct/authconsult.html', {}, context)


def authdiog(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
	
		payi = request.POST['payi']
		

		diogs = Diognosis.objects.filter(gender=payi, is_prescribed=True)
		
		if len(diogs) >= 1:
			diog = True
			return render_to_response('Doct/patientH.html', {'diogs':diogs, 'diog':diog}, context)
		else:
				# An inactive account was used - no logging in!
			msg = "You can call us at 0754307471"
			msg2 = " Send 3,000 to Mobile Number 0754307471"
			authd = True
			return render_to_response('Doct/patientH.html', {'authd':authd, 'msg2': msg2, 'msg': msg}, context)
		

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likey be a HTTP GET.
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		authd=True
		return render_to_response('Doct/patientH.html', {'authd':authd}, context)

def illness(request):
    
    context = RequestContext(request)
    post_values = {}
    password = None
    dname = None
    if request.POST:
		post_values = request.POST.copy()
		
		dname = request.POST['dname']

		comp_signs = request.POST['comp_signs']
		illness = request.POST['illness']
		amb = request.POST['amb']
		gender = request.POST['gender']
		pname = request.POST['pname']
		username = request.POST['username']
		password = request.POST['password']
		role= request.POST['role']
		ptelno = request.POST['telno']
		dname = request.POST['dname']


		if dname == 'Peter':
			dtelno = '+256754307471'
		if dname == 'John':
			dtelno = '+256786031444'
		if dname == 'Anguda':
			dtelno = '+25678603111'

		print "Doctor name %s " % (dname)

		comp_signs = request.POST['comp_signs']
		dpassword = '0754307471'
		dusername = '0754307471'
		dname = 'peter'
		amount =  3000
		enterpay= Enterpay(telno=dusername,amount=amount)
		enterpay.save()
		pay_id = enterpay.id
		gender = pay_id
		ill_det=Illness(gender=gender,comp_signs=comp_signs, illness=illness, page=0,pname=pname,username=username,dtelno=dtelno, dname=dname, amt=amount)
		ill_det.save()
		gender = ill_det.gender	
		ill_id = ill_det.id	
		amb = request.POST['amb']
		diog=Diognosis(page=0,ill_id=ill_id,comp_signs=comp_signs, gender='0',dtelno = dtelno,  diognosis=illness,amb=amb,username=username, dname=dname, illness=illness)
		diog.save()
		print 'Username %s ' % diog.username

		pdiogs = Diognosis.objects.filter(id=diog.id).order_by("id")[:10]
		qconvs = converse.objects.filter(username=username,dusername=dname).order_by("id")[:10]
		msg = "A patient has just contacted us"	
		try:
			mem=convMembers.objects.get(mem_username=username)	
		except Exception,e:
			mem=convMembers(mem_username = username)
			mem.save()

		success_message(
                request, 'process_illness', {'pay_id': pay_id})
        
		# send_illness_sms_notification(request,
  #            msg)
		illness_delivered_email(request, msg)

		return render_to_response('Doct/illdecsuccess.html', { 'pay_id':pay_id,'password':password,'gender':gender, 'pdiogs':pdiogs, 'qconvs':qconvs, 'dname':dname, 'dpassword':dpassword,'pname':pname}, context)


      
	


def patientConverse(request):
	context = RequestContext(request)
	post_values = {}
	pdiog = ''
	pdiogs = ''
	qconv = ''
	qconvs = ''
	pusername=request.POST.get('username', False)
	dusername=request.POST.get('dusername', False)

	pmsg=request.POST.get('pmsg', False)
	dname = "Peter"
        	
	if request.POST:
		pdiogs = Diognosis.objects.filter(username=pusername, doctorusername=dusername)
		qconv = converse(username=pusername, dusername=dusername,pmsg=pmsg)
		qconv.save()
		qconvs = converse.objects.filter(username=pusername).order_by("-id")[:5]



	return render_to_response('Doct/converse.html', { 'dname':dname,'username':pusername, 'dusername':dusername,  'pdiogs':pdiogs,'qconvs':qconvs}, context)

		
          	
 


def add_to_phonebook(request):
    template = settings.BASE_DIR + 'Doct/converse.html'
    response = False
    post_values = {}
    if request.POST:
        post_values = request.POST.copy()
        post_values['user'] = request.user.pk
        form = AddToPhonebookForm(post_values)
        if form.is_valid():
            try:
                check_phonebook = check_phonebook(post_values)
                response = False
                post_values['duplicate'] = True
            except Exception:
                form.save()
                response = True
        else:
            print form.errors
    html = render_to_string(
        template, {'response': response, 'data': post_values})
    return HttpResponse(html)


def ajconv_list(request):
	context = RequestContext(request)
	post_values = {}
	pdiog = ''
	pdiogs = ''
	qconv = ''
	qconvs = ''
	ptelno=request.POST.get('telno', False)
	dtelno=request.POST.get('dtelno', False)

	pmsg=request.POST.get('pmsg', False)
	dname = "Peter"
	template = settings.BASE_DIR + 'templates/Doct/converse.html'
        	
	if request.POST:
		pdiogs = Diognosis.objects.filter(telno=ptelno, doctortelno=dtelno)
		if pmsg:
			qconv = converse(telno=ptelno, phonedoctor=dtelno,pmsg=pmsg)
			qconv.save()
		qconvs = converse.objects.filter(telno=ptelno).order_by("-id")[:5]

	html = render_to_string(
       template, {'dname':dname,'ptelno':ptelno, 'dtelno':dtelno,  'pdiogs':pdiogs,'qconvs':qconvs})

	return HttpResponse(html)

          	 	
    		
   		
   		
        
        
        
	        
def doctConv(request):
	context = RequestContext(request)
	post_values = {}
	pdiog = ''
	pdiogs = ''
	qconv = ''
	qconvs = ''
	pmem = ''
	dusername=request.POST.get('dusername', False)


	dname = "Peter"
        	
	if request.POST:
		post_values = request.POST.copy()
		print "Doctor username %s" % dusername

		try:
			pmem = convMembers.objects.all()
			diogs = Diognosis.objects.all()
		except Exception, e:
			pass

	chatmsg = True
	staf = True
	return render_to_response('Doct/dconverse.html', { 'dname':dname,'dusername':dusername,'pmem':pmem,'chat':chatmsg,'staf':staf, 'diogs':diogs}, context)
			

        	   
	






def Converse(request):
	context = RequestContext(request)
	post_values = {}
	pdiog = ''
	pdiogs = ''
	qconv = ''
	qconvs = ''
	pusername=request.POST.get('username', False)
	dusername=request.POST.get('dusername', False)
	request.session['pusername'] = pusername
	request.session['dusername'] = dusername
	
	if not dusername and not pusername:
		ptelno=request.session['pusername'] 
		dtelno=request.session['dusername']

	pmsg=request.POST.get('pmsg', False)
	dname = "Peter"
        	
	if request.POST:
		post_values = request.POST.copy()
    	form = patientConverseForm(post_values)
        if form.is_valid():
        	
        	
        	try:
        		pdiog = Diognosis.objects.filter(username=pusername, doctorusername=dusername)
        		if len(pdiog) > 0:
        			pdiogs = pdiog
            
                
	        	elif len(pdiog)==1:

	        	
	        		pdiog = pdiog
	        	else:
	        		pass
	        except Exception,e:
	        	diog = Diognosis.objects.get(username=pusername, doctorusername=dusername)

	        qconv = converse(username=pusername, dusername=dusername,pmsg=pmsg)
	        convmem = convMembers(mem_username=pusername, dusername=dusername)
	        try:
	        	memex = convMembers.objects.get(mem_username=pusername)
	        except Exception, e:
	        	convmem.save()
	        	

	        if pmsg:
	        	qconv.save()
       
	        
	        qconvs = converse.objects.filter(username=pusername, dusername=dusername).order_by("-id")[:5]
	        qconvs = reversed(qconvs)



 	
    
	return render_to_response('Doct/converse.html', { 'dname':dname,'pdiog':pdiog,'username':pusername, 'dusername':dusername,  'pdiogs':pdiogs,'qconvs':qconvs}, context)
	






def Converse1(request):
	context = RequestContext(request)
	post_values = {}
	pdiog = ''
	pdiogs = ''
	qconv = ''
	qconvs = ''
	convpfs = ''
	convpf = ''
	telno=request.POST.get('person_telno', '')
	ftelno=request.POST.get('friend_phone', '')

	person_msg=request.POST.get('msg', '')
	dname = "Peter"
	convlog = ''
        	
	if request.POST:
		convlog = Messages(person_phone=telno,msg=person_msg,friend_phone=ftelno)
	
    	

    	if person_msg:
	        	convlog.save()

    	try:

        	convpfs = Messages.objects.filter(Q(person_phone__icontains='' + telno + '') | Q(friend_phone__icontains='' + ftelno + ''))

	

        except Exception,e:
        	convpf  = Messages.objects.get(Q(person_phone__icontains='' + telno + '') | Q(friend_phone__icontains='' + ftelno + ''))

      
       
	       	


	

	return render_to_response('Doct/convtext.html', { 'convpf':convpf,'convpfs':convpfs, 'telno':telno,'ftelno':ftelno}, context)







def convtext(request):
	context = RequestContext(request)
	post_values = {}
	pdiog = ''
	pdiogs = ''
	qconv = ''
	qconvs = ''
	percons = ''
	percon = ''
	telno=request.POST.get('telno', '')
	ftelno=request.POST.get('ftelno', '')

	pmsg=request.POST.get('pmsg', '')
	dname = "Peter"
        	
	if request.POST:
		post_values = request.POST.copy()
	
    	
    	
    	try:
    		convpf = convPersonFrien.objects.filter(Q(person_phone__icontains='' + telno + '') | Q(friend_phone__icontains='' + ftelno + ''))
    		if len(convpf) > 0:
    			convpfs = convpf
        
            
        	elif len(convpf)==1:

        	
        		convpf = convpf
        	else:
        		pass
        except Exception,e:
        	convpf = convPersonFrien.objects.get(Q(person_phone__icontains='' + telno + '') | Q(friend_phone__icontains='' + ftelno + ''))

      
        
        try:

        	percons = Messages.objects.filter(Q(person_phone__icontains='' + telno + '') | Q(friend_phone__icontains='' + ftelno + ''))

	

        except Exception,e:
        	percon  = Messages.objects.get(Q(person_phone__icontains='' + telno + '') & Q(friend_phone__icontains='' + ftelno + ''))

      
       

	

	return render_to_response('Doct/convtext.html', { 'convpf':convpf,'convpfs':convpfs, 'telno':telno,'ftelno':ftelno,'percon':percon, 'percons':percons}, context)





def doctorConverse(request):
	context = RequestContext(request)
	post_values = {}
	pdiog = ''
	pdiogs = ''
	qconv = ''
	qconvs = ''
	ptelno = ''
	dtelno = ''
	noconv = True

	qconv = converse.objects.all()
	  

	if request.POST:
		post_values = request.POST.copy()
    	form = doctorConverseForm(post_values)
        if form.is_valid():
        	ptelno=request.POST.get('telno', False)
        	dtelno=request.POST.get('dtelno', False)
        	dmsg=request.POST.get('dmsg', False)
        	noconv = True
        	try:
        		pdiog = Diognosis.objects.filter(telno=ptelno, doctortelno=dtelno)
        		if len(pdiog) > 0:
        			pdiogs = pdiog
            
                
	        	elif len(pdiog)==1:

	        	
	        		pdiog = pdiog
	        	else:
	        		pass
	        except Exception,e:
	        	diog = Diognosis.objects.get(telno=ptelno, doctortelno=dtelno)

	        form.save()
       
	        try:
	            qconv = converse.objects.filter(telno=ptelno, phonedoctor=dtelno).order_by("id")[:10]
	            if len(qconv) > 1:
	            	qconvs = qconv
	            elif len(qconv) == 1:
	            	qconv = qconv

	        except Exception,e:
	        	print 'nothing', e
	        return render_to_response('Doct/doctConvers.html', { 'pdiog':pdiog,'ptelno':ptelno, 'dtelno':dtelno, 'pdiogs':pdiogs,'qconvs':qconvs, 'qconv':qconv}, context)

                
           


 		    
    
	return render_to_response('Doct/Convers.html', {'qconvs':qconvs, 'qconv':qconv}, context)


def illness_delivered_email(request, msg):
    template = None

    #template = settings.EMAIL_TEMPLATE_DIR + 'transaction.html'
    email = "mandelashaban593@gmail.com"

    mailer(
        request, 'Delivery Notification (es-doctor.com )',
        msg, email)

# def AddIllDet(request):
    
#     context = RequestContext(request)
#     response = False
#     post_values = {}
#     if request.POST:
#         post_values = request.POST.copy()
#         gender = request.POST['gender']
#         kin = request.POST['kin']
#         kintelno = request.POST['kintelno']
#         username = request.POST['username']
#         ill_edit=Illness.objects.get(gender=gender)
#         ill_edit.gender=gender
#         ill_edit.kin  =  kin
#         ill_edit.kintelno = kintelno
#         ill_edit.username = username
#         ill_edit.save()
       
	       
#         ill_et = True
#         return render_to_response('Doct/patientH.html', {'ill_success':ill_success, 'ill_et':ill_et}, context)

   	
    
#     return render_to_response('Doct/patientH.html', { }, context)



def AddIllDet(request):
	context = RequestContext(request)
	gender = request.POST['gender']
	kin = request.POST['kin']
	kintelno = request.POST['kintelno']
	username = request.POST['username']
	ill_success = False
	ill_et = False
	email = request.POST['email']
	ill_edit = get_object_or_404(Illness.objects.filter(gender=gender))

	form = AddIllDetForm()
	if request.POST:
		form = AddIllDetForm(request.POST, instance=ill_edit)
        if form.is_valid():
        	form.save()
        	ill_et = True
        	
			
            
         	return render_to_response('Doct/patientH.html', {'ill_et':ill_et}, context)

	return render_to_response('Doct/patientH.html', { }, context)

           

    
def view_illness(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	ill = Illness.objects.all()
	if ill:
		msg = "Illness records"
		return render_to_response('Doct/view_illness.html', {'ill':ill, 'msg':msg}, context)
	else:
		msg = "No Illness record"
		return render_to_response('Doct/doctorH.html', {'msg':msg}, context)

def custom_404(request):

	return handler404(request)

def handler404(request):
    response = render_to_response('Doct/my404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response



def doct_view_illness(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	doct_ill = False
	ill = Illness.objects.all()
	if ill:
		msg = "Illness records"
		doctview_ill = True
		return render_to_response('Doct/doctorH.html', {'doctview_ill':doctview_ill}, context)
	else:
		msg = "No Illness record"
		doct_ill = True
		return render_to_response('Doct/doctorH.html', {'doct_ill':doct_ill, 'ill':ill}, context)



def view_illness2(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	doct_ill = False
	ill = Illness.objects.all()
	paginator = Paginator(ill, settings.PAGNATION_LIMIT)
	page = request.GET.get('page')
	try:
		ill = paginator.page(page)
	except PageNotAnInteger:
		ill = paginator.page(1)
		# If page is not an integer, deliver first page.
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		ill = paginator.page(paginator.num_pages)

	if ill:
		msg = "Illness records"
		doctview_ill = True
		staf = True
		return render_to_response('Doct/index_staff.html', {'doctview_ill':doctview_ill, 'ill':ill,'staf':staf}, context)
	else:

		msg = "No Illness record"
		doct_ill = True
		return render_to_response('Doct/doctorH.html', {'doct_ill':doct_ill, 'ill':ill}, context)


def ind_illness(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	ind_ill = False
	ill = Illness.objects.all().order_by('-id')
	indill_auth = False
	staf = False
	if request.POST:
		username = request.POST['username']
		ill = Diognosis.objects.filter(telno=username).order_by('-id')

		paginator = Paginator(ill, settings.PAGNATION_LIMIT)
		page = request.GET.get('page')
		try:
			ill = paginator.page(page)
		except PageNotAnInteger:
			ill = paginator.page(1)
			# If page is not an integer, deliver first page.
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			ill = paginator.page(paginator.num_pages)

		if len(ill) > 1:
			ind_ill = True
			staf = True
			msg = "Illness records"
			return render_to_response('Doct/viewind_ill.html', {'ill':ill, 'ind_ill':ind_ill, 'msg':msg,'staf':staf}, context)
		
		ind_illrecs = True
		staf = True
		msg = "Illness records"
		return render_to_response('Doct/viewind_ill.html', {'ill':ill, 'ind_illrecs':ind_illrecs, 'msg':msg,'staf':staf}, context)
	
	else:
		msg = "No Illness record"
		indill_auth = True
		staf=True
		return render_to_response('Doct/index_staff.html', {'msg':msg, 'indill_auth':indill_auth, 'ill':ill, 'staf':staf}, context)

# def Expillness(request):
# 	# Like before, obtain the context for the user's hrequest.
# 	context = RequestContext(request)
	
# 	expill = True
# 	return render_to_response('Doct/patientH.html', {'expill':expill}, context)

def tellillness(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	exill = True
	return render_to_response('Doct/patientH.html', {'exill':exill}, context)
	

def authindillness(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	authindill = True
	return render_to_response('Doct/diog.html', {'authindill':authindill}, context)

def diogform(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	dform = True
	return render_to_response('Doct/doctorH.html', {'dform':dform}, context)


# def diognosis(request):
# 	# Like before, obtain the context for the user's hrequest.
# 	context = RequestContext(request)
# 	msg = ''
# 	msg2 = ''

# 	# If the request is a HTTP POST, try to pull out the relevant information.
# 	if request.method == 'POST':
# 		dname = request.POST['dname']
# 		telno = request.POST['telno']
# 		gender = request.POST['gender']
# 		diognosis = request.POST['diognosis']
# 		page = request.POST['page']
# 		payi = request.POST['payi']
# 		email = request.POST['email']
# 		# Gather the username and password provided by the user.
# 		diognosis = Diognosis(dname=dname,telno=telno, gender=gender, diognosis=diognosis, page=page,payi=payi,email=email)
	
# 		if diognosis:
# 			# Save the user's form data to the database.
# 			diognosis = diognosis.save()
			
# 			diognosis = True
# 			msg="You have successfully submitted diognosis"

# 			return render_to_response('rango/diog.html', {'diognosis':diognosis, 'msg':msg}, context)
# 			#return HttpResponseRedirect(reverse('authConsult'))

# 		else:
# 			pass
			

# 	else:
# 		pass
		

# 	return render_to_response('rango/diog.html', {}, context)	

@ajax_required
def diognosis(request):
    template = 'Doct/add_diognosis.html'
    response = False
    post_values = {}
    if request.POST:
        post_values = request.POST.copy()
        form = DiognosisForm(post_values)
        if form.is_valid():
            try:
                check_diognosis = check_diognosis(post_values)
                response = False
                post_values['duplicate'] = True
            except Exception:
                form.save()
                response = True
        else:
            print form.errors
    html = render_to_string(
        template, {'response': response, 'data': post_values})
    return HttpResponse(html)



def view_diognosis(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	diogs = Diognosis.objects.all()
	if diogs:
		msg = "Diognosis records"
		return render_to_response('Doct/view_diog.html', {'diogs':diogs, 'msg':msg}, context)
	else:
		msg = "No Diognosis record"
		return render_to_response('Doct/view_diog.html', {'msg':msg}, context)



def receipt(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	rec = False

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		id = request.POST['id']
		id = int(id)
		

		p = Enterpay.objects.get(id=id)
		
		entp = True

		if p:
		
			return render_to_response('Doct/vp_receipt.html', {'p':p, 'entp':entp}, context)
		else:
				# An inactive account was used - no logging in!
			msg = "Wrong number or or no receipt"
			msg2 = "You can call us at 0754307471"
			return render_to_response('Doct/receiptform.html', {'msg':msg, 'msg2': msg2}, context)
		

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likey be a HTTP GET.
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...

		return render_to_response('Doct/receipt1.html', {}, context)


def index_receipt(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	recfm = False

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		id = request.POST['id']
		id = int(id)
		

		p = Enterpay.objects.get(id=id)
		
		entp = True

		if p:
		
			return render_to_response('Doct/patientH.html', {'p':p, 'entp':entp}, context)
		else:
				# An inactive account was used - no logging in!
			msg = "Wrong number or or no receipt"
			msg2 = "You can call us at 0754307471"
			return render_to_response('Doct/receiptform.html', {'msg':msg, 'msg2': msg2}, context)
		

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likey be a HTTP GET.
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		recfm = True
		return render_to_response('Doct/index_base.html', {'recfm':recfm}, context)


def doctor_receipt(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	dot_rec = False

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		id = request.POST['id']
		id = int(id)
		
		p = Enterpay.objects.get(id=id)
		
		entp = True
		staf = True

		if p:
			
			return render_to_response('Doct/view_receipt.html', {'p':p,'staf':staf,'entp':entp}, context)
		else:
				# An inactive account was used - no logging in!
			msg = "Wrong number or or no receipt"
			msg2 = "You can call us at 0754307471"
			return render_to_response('Doct/doctor_authreceipt.html', {'msg':msg, 'msg2': msg2}, context)
		

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likey be a HTTP GET.
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		dot_rec = True
		staf = True 
		return render_to_response('Doct/index_staff.html', {'dot_rec':dot_rec, 'staf':staf}, context)


def delP(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	delete = False


	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		


		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		
		p = Register.objects.filter(username=username)
		
		# If we have  a User object, the details are correct.
		# if None (Python's  way of  representing the absent of a value), no user
		# with matching credentials was found.
		if p.delete():
			delete = True
			msg = "User deleted successfully"
			return render_to_response('Doct/adminH.html', {'msg':msg, 'delete':delete}, context)
		else:
				# An inactive account was used - no logging in!
			msg = "Incorrect username"

			
			return render_to_response('Doct/delp.html', {'msg':msg, 'delete':delete}, context)
		

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likey be a HTTP GET.
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		return render_to_response('Doct/delp.html', {}, context)
		


def patientD(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	role='patient'
	p = Register.objects.filter(role=role)
	if p:
		msg = "Patient records"
		return render_to_response('Doct/patientD.html', {'p':p, 'msg':msg}, context)
	else:
		msg = "No patient record"
		return render_to_response('Doct/patientD.html', {'msg':msg}, context)



def admin_pat(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	role='patient'
	p = Register.objects.filter(role=role)
	paginator = Paginator(p, settings.PAGNATION_LIMIT)
	page = request.GET.get('page')
	try:
		p = paginator.page(page)
	except PageNotAnInteger:
		p = paginator.page(1)
		# If page is not an integer, deliver first page.
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		p = paginator.page(paginator.num_pages)
	if p:
		msg = "Patient records"
		return render_to_response('Doct/view_pat.html', {'p':p, 'msg':msg}, context)
	else:
		msg = "No patient record"
		return render_to_response('Doct/adminH.html', {'msg':msg}, context)


def admin_doct(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg1 = ''
	role='doctor'
	d = Register.objects.filter(role=role)
	paginator = Paginator(d, settings.PAGNATION_LIMIT)
	page = request.GET.get('page')
	try:
		d = paginator.page(page)
	except PageNotAnInteger:
		d = paginator.page(1)
		# If page is not an integer, deliver first page.
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		d = paginator.page(paginator.num_pages)

	if d:
		msg = "Doctor records"
		return render_to_response('Doct/view_doct.html', {'d':d, 'msg':msg}, context)
	else:
		msg1 = "No Doctor record"
		return render_to_response('Doct/adminH.html', {'msg1':msg1}, context)

def adminH(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	
	return render_to_response('Doct/adminH.html', {'msg':msg}, context)


def doctorD(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg1 = ''
	role='doctor'

	d = Register.objects.filter(role=role)
	if d:
		msg = "Doctor Details"
		return render_to_response('Doct/adminH.html', {'d':d, 'msg':msg}, context)
	else:
		msg1 = "No Doctor record"
		return render_to_response('Doct/adminH.html', {'msg1':msg1}, context)


def patientH(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	return render_to_response('Doct/patientH.html', {}, context)

def doctorH(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	return render_to_response('Doct/doctorH.html', {}, context)


def about(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	return render_to_response('Doct/about.html', {}, context)


def whyus(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	return render_to_response('Doct/whyus.html', {}, context)


def contact(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	post_values = ''
        

	
	return render_to_response('Doct/contactus.html', {}, context)

def our_team(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	return render_to_response('Doct/ourteam.html', {}, context)



def enterpay(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	enterpay = False
	pill = ''
	r = ''
	reg = ''
	pdiog =  ''
	ill_more = False
	patlog = False
	pdiogs = None
	nodiog = False
	qconv = None
	qconvs = None

	# If the request is a HTTP POST, try to pull out the relevant information.
	post_values = request.POST.copy()
	form = LoginForm()

	if request.method == 'POST':
		# Gather the username and password provided by the user.
		telno = request.POST['telno']
		role = request.POST['role']
		form = LoginForm(post_values)

		try:
			r = Register.objects.get(telno=telno)
		except Exception, e:
			print "Account  doesn't exist", e

		try:
			pdiogs = Diognosis.objects.filter(telno=telno)

		except Exception, e:
			print "diog doesn't exist", e

		try:
			qconvs = converse.objects.filter(telno=telno).order_by("id")[:5]
			
		except Exception,e:
			print 'nothing', e


		if r:
			if r.role=='patient':
				patlog=True
				ill_more = True
				print "Role %s " % (r.role)
			return render_to_response('Doct/patientH.html', {'ptelno':telno,'nodiog':nodiog,'pdiogs':pdiogs,'patlog':patlog,'ill_more':ill_more,'qconvs':qconvs}, context)
		else:
			if form.is_valid():
				form.save()
			ill_more = True

			 # return HttpResponse(response)
			return render_to_response('Doct/patientH.html', {'ptelno':telno,'pdiogs':pdiogs,'patlog':patlog,'reg':reg, 'ill_more':ill_more, 'qconvs':qconvs}, context)


	else:
		pass

	pay=True

	return render_to_response('Doct/payconsult.html', {'pay':pay}, context)	




def enterpay2(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	enterpay = False
	pill = ''
	r = ''
	reg = ''
	pdiog =  ''
	ill_more = False
	patlog = False
	pdiogs = None
	nodiog = False
	qconv = None
	qconvs = None
	username=  None

	# If the request is a HTTP POST, try to pull out the relevant information.
	post_values = request.POST.copy()
	form = LoginForm()

	if request.method == 'POST':
		# Gather the username and password provided by the user.
	
		role = request.POST['role']

		username = request.POST['username']
		password = request.POST['password']

		print 'Username %s ' % username
		print 'Password %s ' % password

		form = LoginForm(post_values)
		user_form = UserForm(data=request.POST)

		try:
			r = Register.objects.get(password=password)
		except Exception, e:
			print "Account  doesn't exist", e

		try:
			pdiogs = Diognosis.objects.filter(username=username)
			for pdiog in pdiogs:
				print 'Username  %s ' % pdiog.username
			
				

		except Exception, e:
			print "diogs doesn't exist", e

		try:
			for pdiog in pdiogs:
				print ' Username ', pdiog.username
		except Exception, e:
			print 'No attribute username', e
				


		try:

			pdiog = Diognosis.objects.get(username=username)
			print ' Username %s'   % (pdiog.username)

		except Exception, e:
			print "diog doesn't exist", e




		try:
			qconvs = converse.objects.filter(username=username).order_by("id")[:5]

			
		except Exception,e:
			print 'nothing', e




		if r:

			ill_more = True
			print "Role %s " % (r.role)
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					if pdiogs:

						return render_to_response('Doct/patientsub.html', {'password':password,'nodiog':nodiog,'pdiogs':pdiogs,'pdiog':pdiog,'patlog':patlog,'ill_more':ill_more,'qconvs':qconvs}, context)
					else:
						return render_to_response('Doct/patientH.html', {'password':password,'nodiog':nodiog,'pdiogs':pdiogs,'pdiog':pdiog,'patlog':patlog,'ill_more':ill_more,'qconvs':qconvs}, context)

		
		else:
			if user_form.is_valid():
				form.save()
				u = User(username=username, password=password)
				u.save()
			ill_more = True

			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					if pdiogs:
						return render_to_response('Doct/patientsub.html', {'password':password,'nodiog':nodiog,'pdiogs':pdiogs,'pdiog':pdiog,'patlog':patlog,'ill_more':ill_more,'qconvs':qconvs}, context)
					else:
						return render_to_response('Doct/patientH.html', {'password':password,'nodiog':nodiog,'pdiogs':pdiogs,'pdiog':pdiog,'patlog':patlog,'ill_more':ill_more,'qconvs':qconvs}, context)

		
				else:
					return render_to_response('Doct/index.html', {}, context)
			else:
				print 'User does not exist'




			 # return HttpResponse(response)
			

	else:
		pass

	pay=True

	return render_to_response('Doct/index.html', {'pay':pay}, context)	




def register(request):
	# Like before, get the request's context.
	context = RequestContext(request)
	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False

	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
	
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()
			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user
			rg = Register(user=user,username=username, password=password, email=email, page='0', role="patient")
			rg.save()
			print 'Password %s' % rg.password
			print 'Password %s' % rg.username
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserPro
			registered = True
		else:
			print user_form.errors, profile_form.errors
			# Not a HTTP POST, so we render our form using two ModelForm instances.
			# These forms will be blank, ready for user input.

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
		# Render the template depending on the context.
	return render_to_response(
	'Doct/register.html',
	{'user_form': user_form, 'registered': registered},
	context)







def editdiog(request,diog_id=1, ill_id=1):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	staf = False

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'GET':
		
		ediog = Diognosis.objects.get(id=diog_id)
		illpay = Illness.objects.get(id=ill_id)
		
		editD = True
		staf = True 
		
		return render_to_response('Doct/index_staff.html', {'ediog':ediog,'illpay':illpay, 'editD':editD, 'staf':staf}, context)
		
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		return render_to_response(' ', {}, context)

def follup(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	fup = True

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		gender=request.POST['gender']
		fupm=request.POST['fup']
		
		fmsg = Diognosis.objects.get(gender=gender)
		fmsg.fup=fupm
		fmsg.save()
		msg2="You have sent a follow up message"
		
		
		
		return render_to_response('Doct/fup.html', {'msg2':msg2, 'fup':fup}, context)
		
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		
		return render_to_response('Doct/fup.html', {'fup':fup}, context)

def repmsg(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	reply = True
	fupmsg = ''
	ptelno= ''

	try:
		fupmsg = Diognosis.objects.get(gender=gender)
		ptelno = fupmsg.telno
	except Exception, e:
		print e

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		gender=request.POST['gender']
		try:
			fupmsg = Diognosis.objects.get(gender=gender)
			ptelno = fupmsg.telno

			return render_to_response('Doct/view_fup.html', {'fupmsg':fupmsg, 'ptelno':ptelno}, context)
		except Exception, e:
			
			error_message(request, 'cons_error', {})
			return render_to_response('Doct/repmsg.html', {'msg2':msg2}, context)
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		
		
		return render_to_response('Doct/repmsg.html', {'ptelno':ptelno}, context)



def sendmessage(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	reply = True

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		send=request.POST['send']

		try:
			send = converse(msg=send)
			send.save()

			return render_to_response('Doct/view_fup.html', {'fupmsg':fupmsg}, context)
		except Exception, e:
			msg2 = "No doctor message messages for this chat"
			return render_to_response('Doct/repmsg.html', {'msg2':msg2}, context)
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		
		
		return render_to_response('Doct/repmsg.html', {}, context)




def sendrep(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	reply = True
	qconvs = ''
	dtelno = ''
	ptelno = ''
	pmsg = ''
	staf = False

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		dmsg=request.POST.get('dmsg', False)
		pusername=request.POST.get('pusername', False)
		dusername=request.POST.get('dusername', False)
		staf = True
		try:
			msg = converse(dmsg=dmsg,username=pusername,dusername=dusername)
			msg.save()
			qconvs = converse.objects.filter(username=pusername,dusername=dusername).order_by('-id')[:5]
			qconvs = reversed(qconvs)
			return render_to_response('Doct/convdoct.html', {'qconvs':qconvs, 'pusername':pusername, 'dusername':dusername,'staf':staf}, context)
		except Exception, e:
			msg2 = "No doctor message messages for this chat"
			return render_to_response('Doct/convdoct.html', {'qconvs':qconvs, 'pusername':pusername, 'dusername':dusername,'staf':staf}, context)
	else:
		pass

		
		

def sendrep2(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	reply = True
	qconvs = ''
	dtelno = ''
	ptelno = ''
	pmsg = ''
	import json as simplejson

	print "Mesaage  0"

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'GET':
		dmsg=request.GET.get('dmsg', False)
		ptelno=request.GET.get('telno', False)
		dtelno=request.GET.get('dtelno', False)
		try:
			msg = converse(dmsg=dmsg,telno=ptelno,phonedoctor=dtelno)
			msg.save()

			print "Mesaage  1", msg.dmsg
		


			qconvs = converse.objects.filter(telno=ptelno,phonedoctor=dtelno).order_by('-id')[:5]
			qconvs = reversed(qconvs)

			html = render_to_string( 'Doct/convdoct.html', {'qconvs':qconvs, 'ptelno':ptelno, 'dtelno':dtelno})
			
			return HttpResponse(html)
	        
	        

		except Exception, e:
			msg2 = "No doctor message messages for this chat"
			return render_to_response('Doct/convdoct.html', {'qconvs':qconvs, 'ptelno':ptelno, 'dtelno':dtelno}, context)
	else:
		pass


def ajDoctconv_list(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	reply = True
	qconvs = ''
	dtelno = ''
	ptelno = ''
	pmsg = ''
	template = settings.BASE_DIR + 'templates/Doct/convdoct.html'

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		dmsg=request.POST.get('dmsg', False)
		ptelno=request.POST.get('telno', False)
		dtelno=request.POST.get('dtelno', False)
		try:
			if msg:

				msg = converse(dmsg=dmsg,telno=ptelno,phonedoctor=dtelno)
				msg.save()
			qconvs = converse.objects.filter(telno=ptelno,phonedoctor=dtelno).order_by('-id')[:5]
			qconvs = reversed(qconvs)
			html = render_to_string(
        	template, {'qconvs':qconvs, 'ptelno':ptelno, 'dtelno':dtelno})

        	
		except Exception, e:
			msg2 = "No doctor message messages for this chat"
			return render_to_response('Doct/convdoct.html', {'qconvs':qconvs, 'ptelno':ptelno, 'dtelno':dtelno}, context)
	else:
		pass

	return HttpResponse(html)








def dviewmsg(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	qconvs= ''

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		pusername=request.POST.get('mem_username', False)

		qconvs=converse.objects.filter(username=pusername).order_by('-id')[:5]
		qconvs = reversed(qconvs)
		
		replyD = True
		staf = True
		
		return render_to_response('Doct/convdoct.html', { 'qconvs':qconvs, 'pusername':pusername, 'staf':staf}, context)
		
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		return render_to_response('Doct/doctorH.html', {}, context)



	
def edited_diog(request):
    editd_response = False
    context = RequestContext(request)
    post_values = request.POST.copy()
    diognosis  = '	'
    if request.POST:
        id = request.POST['id']
        dname = request.POST['dname']
        telno = request.POST['telno']
        gender = request.POST['gender']
        dio = request.POST['diognosis']
        page = request.POST['page']
        email = request.POST['email']
        amb = request.POST['amb']
        fup = request.POST['fup']
        try:
            diognosis = Diognosis.objects.get(id=id)
        except Exception, e:
            pass
        if diognosis:
	        diognosis.id=id
	        diognosis.dname=dname
	        diognosis.doctortelno=telno
	        diognosis.gender=gender
	        diognosis.diognosis=dio
	        diognosis.page=page
	        diognosis.email=email
	        diognosis.amb=amb
	        diognosis.fup=fup
	        diognosis.is_prescribed=True
	        diognosis.save()
	        editd_response = True
	        diog = Diognosis.objects.all().order_by('-id')
	        staf = True
	        messages.success(
            request, "The patient medication was successfully prescribed")

	        return render_to_response('Doct/index_staff.html', {'editd_response': editd_response, 'diogs': diog, 'staf':staf}, context)

    else:
    	pass

	return render_to_response('Doct/doctorH.html', {'editd_response': editd_response}, context)
@login_required
def restricted(request):

	context=RequestContext(request)



	return render_to_response('Doct/restricted.html', { 'note': 'Wow you are already logged in' }, context)



# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return HttpResponseRedirect('/Doct/')



def ambulance(request):

	context=RequestContext(request)
	if request.POST:
	    districts = request.POST['districts']
	    place = request.POST['place']
	    phone = request.POST['phone']
	    amb=Ambulance(districts=districts,place=place,phone=phone)
	    amb.save()
	    
		
		

	return render_to_response('Doct/patientH.html', { 'amb_msg': 'Ambulance will come to pick you now' }, context)



def convbaddy(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	response = None
	log = False
	convmem = ''
	phonedoctor = ''
	checkfnd = ''
	checkfnd2 = ''
	telno = ''

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		telno = request.POST['telno']
		names = request.POST['names']
		
	
		try:
			convmem = convReg.objects.get(mem_phone=telno)

			try:
				checkfnd = convPersonFrien.objects.filter(person_phone=telno).order_by("id")[:10]
				if len(checkfnd) == 1:
					checkfnd2 = checkfnd	

			except Exception, e:
				checkfnd = ''
			checkfnd = convPersonFrien.objects.filter(person_phone=telno).order_by("id")[:10]
			return render_to_response('Doct/conversefnds.html', {'checkfnd':checkfnd, 'checkfnd2':checkfnd2, 'telno':telno}, context)
		except Exception, e:
			convmem = convReg(mem_phone=telno, names=names)
			convmem.save()
			checkfnd = convPersonFrien.objects.filter(person_phone=telno).order_by("id")[:10]
			return render_to_response('Doct/conversefnds.html', {'checkfnd':checkfnd, 'checkfnd2':checkfnd2, 'telno':telno}, context)



	log = True
	return render_to_response('Doct/convbaddy.html', {'log':log}, context)



def searchPhone(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	response = None
	log = False
	convmem = ''
	phonedoctor = ''
	checkfnd = ''
	checkfnd2 = ''
	checkfnds= ''


	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		telno = request.POST['telno']
		number = request.POST['number']
		print "Tel 1 %s" % telno
		print "Friend Tel 2 %s" % number

		

		try:
			convmem = convReg.objects.get(mem_phone=number)
			checkfnd = convPersonFrien.objects.filter(friend_phone=number, person_phone=telno)
			
		except Exception, e:
			print e

		try:
			if not checkfnd and convmem:

				checkfnd = convPersonFrien(friend_phone=number, person_phone=telno)	
				checkfnd.save()
				checkfnd = convPersonFrien.objects.filter(person_phone=telno)
				if len(checkfnd) == 1:
					checkfnd2 = checkfnd
				return render_to_response('Doct/conversefnds.html', {'checkfnd2':checkfnd2,'checkfnd':checkfnd, 'telno':telno}, context)

		except Exception, e:
			print e

		checkfnd = convPersonFrien.objects.filter(person_phone=telno)
		if len(checkfnd) == 1:
			checkfnd2 = checkfnd
		
		return render_to_response('Doct/conversefnds.html', {'checkfnd':checkfnd,'telno':telno, 'checkfnd2':checkfnd2}, context)




	log = True
	return render_to_response('Doct/convbaddy.html', {'log':log}, context)





    	
def change_stuff_telephone(request, is_customer_care=False):
    '''create an admin user'''
    context = RequestContext(request)
    success = False

    form = ''
    if request.POST:
        form = ChangeAdminTelephoneForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.save()
            user.is_staff = True
            # user.save()
            # assign user permissions
            update = False
            assign_permissions(user, form, update, is_customer_care)
            user.save()

            # save profile options
            profile = AdminProfile(user=user)
            profile.is_customer_care = is_customer_care
            # if form.cleaned_data['reports'] == '2':
            #    profile.is_customer_care = True
            if not form.cleaned_data['country'] == '1':
                profile.country = form.cleaned_data['country']
            if not form.cleaned_data['network'] == '1':
                profile.mobile_network = form.cleaned_data['network']
            profile.save()
            # user = form.save()
            # user.is_staff = True
            # user.save()
            # debug(user)
            messages.success(request, "The User Was Successfully Created")
            success = True
    super_admin = True
    return render_to_response('Doct/change_stuff_telephone.html', {'form': form,'success':success, 'super_admin':super_admin},context)




def addcontact(request):
    template = settings.AJAX_TEMPLATE_DIR + 'addcontact.html'
    response = False
    post_values = {}
    context = RequestContext(request)

    if request.POST:
        post_values = request.POST.copy()
        telno = post_values['telno']
        email = post_values['email']
        name = post_values['name']
        msg = post_values['msg']
        print "Message %s " %  msg
        
    	cont=Contact(telno=telno,email=email, msg=msg)
    	cont.save()
    	response = True

    	if cont:
    		messages.success(request, "Your contact details have been Successfully added")
            
            
        else:
        	messages.success(request, "Error occured while adding your contact details")
          


    return render_to_response('Doct/contactus.html', {}, context)



def orderdrugs(request):
    
    response = False
    post_values = {}
    context = RequestContext(request)

    if request.POST:
        post_values = request.POST.copy()
        telno = post_values['telno']
        location = post_values['location']
        msg = post_values['msg']
        print "Message %s " %  msg
        
    	cont=Orderdrugs(telno=telno,location=location, msg=msg)
    	cont.save()
    	response = True

    	if cont:
    		messages.success(request, "Your have been Successfully ordered for drugs")
            
            
        else:
        	messages.success(request, "Error occured while ordering for drugs")
          


    return render_to_response('Doct/orderdrugs.html', {}, context)




def labtests(request):
    
    response = False
    post_values = {}
    context = RequestContext(request)

    if request.POST:
        post_values = request.POST.copy()
        telno = post_values['telno']
        location = post_values['location']
        msg = post_values['msg']
        print "Message %s " %  msg
        
    	cont=Labtests(telno=telno,location=location, msg=msg)
    	cont.save()
    	response = True

    	if cont:
    		messages.success(request, "You have been Successfully ordered for Lab tests")
            
            
        else:
        	messages.success(request, "Error occured while ordering for Lab tests")
          


    return render_to_response('Doct/labtests.html', {}, context)





def test(request):
    template = settings.AJAX_TEMPLATE_DIR + 'addcontact.html'
    response = False
    post_values = {}
    context = RequestContext(request)
    cont = None
    if request.GET:
        post_values = request.GET.copy()
        telno = post_values['fname']
        email = post_values['lname']
        msg = post_values['msg'] = 0
        print "Contact view reached" 
        
    	cont=Contact(telno=telno,email=email, msg=msg)
    	cont.save()
    	response = True
    	cont = Contact.objects.get(id=cont.id)

    	if cont:
    		messages.success(request, "Your have Successfully tested")
            
            
        else:
        	messages.success(request, "Error occured while testing")

        return HttpResponse(
        json.dumps(post_values),
        content_type="application/json"
	    )
          


    return render_to_response('Doct/test.html', {'cont':cont}, context)