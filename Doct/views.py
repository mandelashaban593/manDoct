# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from Doct.models import Category
from Doct.decorators import ajax_required, login_required
from django.http import HttpResponse

from Doct.models import Page, UserProfile, Topup,Register, Enterpay,Illness, Diognosis,Conddrugs

from Doct.forms import CategoryForm, UserForm,DiognosisForm
from Doct.forms import PageForm, TopupForm, PatientForm, IllnessForm,DoctorForm,AddIllDetForm
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
from Doct.utils import check_illness

def index(request):


	#obtain the Context from the HTTP request
	context=RequestContext(request)


	# Query for categories- add the list to our context dictionary.
	category_list=Category.objects.all()
	context_dict={'categories': category_list}

	# The following two lines are new
	# We loop through each category returned, and create a URL attribute.
	# This attribute stores an encoded URL (e.g spaces replaced with underscores).
	for category in category_list:
		category.url = category.name


	page_list = Page.objects.order_by('-views')[:0]
	context_dict['pages'] = page_list

	#### NEW CODE ###
	if request.session.get('last_visit'):
		# The session has a value for the last visit
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits', 0)
		
		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
			request.session['visits'] = visits + 1
			request.session['last_visit'] = str(datetime.now())
	else:
		# The get returns None, and the session does not have a value for the last visit.
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1
	#### END NEW CODE ###


	# Render and return the rendered response back to the user.
	return render_to_response('Doct/index.html', context)
	
	

def category(request, category_name_url):
	context=RequestContext(request)

	category_name=category_name_url.replace('_', ' ')

	context_dict={'category_name': category_name}


	try:

		category=Category.objects.get(name=category_name)
		pages=Page.objects.filter(category=category)

		context['pages']=pages;
		context['category']=category

	except Category.DoesNotExist:

		pass



	return render_to_response('Doct/category.html', context_dict, context)


def add_category(request):
	# Get the context from the request

	context=RequestContext(request)


	# A HTTP POST?
	if request.method=='POST':
		form=CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)


			# Now call the index() view.
			# The user will be shown the homepage.
			return index(request)
		else:
			# The supplied form contained errors- Just print them to the terminal.
			print form.errors
	else:
		# if the request was not a POST, display the form to enter details.
		form=CategoryForm()

	# Bad form(or form details), no form supplied...
	# Render the form with error messages (if any).
	return render_to_response('Doct/add_category.html', {'form':form}, context)



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


	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		password = request.POST['password']
		username = request.POST['username']
		r = None	

		

		try:
			r = Register.objects.get(password=password)
		except Exception, e:
			print "Invalid Username Or Password", e

		if r:
			if r.role=='patient':
				patlog=True
				return render_to_response('Doct/patientH.html', {'patlog':patlog}, context)
			elif r.role =='doctor':
				doctlog=True
				diog = Diognosis.objects.all().order_by('-id')
				return render_to_response('Doct/doctorH.html', {'diog':diog, 'doctlog':doctlog}, context)
			elif r.role =='admin':
				adlog = True
				return render_to_response('Doct/adminH.html', {'adlog':adlog}, context)
			else:
				return render_to_response('Doct/index.html', {}, context)
		else:
			 messages.error(request,
                                    "Incorrect username or password"
                                    )
			 response = True
			 # return HttpResponse(response)
			 return render_to_response('Doct/index.html', {'response':response}, context)


	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
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
		

		diogs = Diognosis.objects.filter(gender=payi)
		
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
    response = False
    illmsg  = False
    illmsg = ''
    exill = False
    ill_success = False
    post_values = {}
    if request.POST:

        post_values = request.POST.copy()
        illness = request.POST['illness']
        gender = request.POST['gender']
        page = request.POST['page']
        ill_det=Illness(gender=gender, illness=illness, page=page)
        ill_det.save()
        gender = ill_det.gender
        cdrugs=Conddrugs.objects.get(cond=illness)
	  	
        amb = request.POST['amb']
        drugs=cdrugs.drugs
        diog=Diognosis(gender=gender,page=page,diognosis=drugs,amb=amb)
        diog.save()
      	return render_to_response('Doct/addill.html', {'ill_success':ill_success, 'gender':gender}, context)
		
	
	exill=True

    	
    return render_to_response('Doct/patientH.html', {'exill':exill}, context)


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

	return True

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
	if ill:
		msg = "Illness records"
		doctview_ill = True
		return render_to_response('Doct/doctorH.html', {'doctview_ill':doctview_ill, 'ill':ill}, context)
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
	if request.POST:
		username = request.POST['username']
		ill = Illness.objects.filter(username=username)
		if len(ill) > 1:
			ind_ill = True
			msg = "Illness records"
			return render_to_response('Doct/doctorH.html', {'ill':ill, 'ind_ill':ind_ill, 'msg':msg}, context)
		else:
			ind_illrecs = True
			msg = "Illness records"
			return render_to_response('Doct/doctorH.html', {'ill':ill, 'ind_illrecs':ind_illrecs, 'msg':msg}, context)
		
	else:
		msg = "No Illness record"
		indill_auth = True
		return render_to_response('Doct/doctorH.html', {'msg':msg, 'indill_auth':indill_auth, 'ill':ill}, context)

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

		return render_to_response('Doct/receiptform.html', {'rec':rec}, context)


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

		if p:
		
			return render_to_response('Doct/view_receipt.html', {'p':p, 'entp ':entp}, context)
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
		return render_to_response('Doct/doctorH.html', {'dot_rec':dot_rec}, context)


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
	if p:
		msg = "Patient records"
		return render_to_response('Doct/adminH.html', {'p':p, 'msg':msg}, context)
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
	if d:
		msg = "Doctor records"
		return render_to_response('Doct/admin_doctorD.html', {'d':d, 'msg':msg}, context)
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

def contact(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	
	return render_to_response('Doct/contactus.html', {}, context)

def enterpay(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''
	enterpay = False

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		telno = request.POST['telno']
		amount = request.POST['amount']
		enterpay= Enterpay(telno=telno, amount=amount)
		enterpay.save()
		pay_id = enterpay.id
		
		enterpay = True
		expill = True
		msg1="You have successfully submitted payment Details, Print Receipt"

		return render_to_response('Doct/patientH.html', {'enterpay':enterpay, 'msg1':msg1, 'pay_id':pay_id, 'expill':expill}, context)
		#return HttpResponseRedirect(reverse('authConsult'))

	

	else:
		pass

	pay=True

	return render_to_response('Doct/payconsult.html', {'pay':pay}, context)	



def editdiog(request,diog_id=1):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	msg2 = ''

	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'GET':
		
		ediog = Diognosis.objects.get(id=diog_id)
		
		editD = True
		
		return render_to_response('Doct/doctorH.html', {'ediog':ediog, 'editD':editD}, context)
		
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object ...
		return render_to_response('Doct/DoctorH.html', {}, context)
	
def edited_diog(request):
    editd_response = False
    context = RequestContext(request)
    post_values = request.POST.copy()
    if request.POST:
        id = request.POST['id']
        dname = request.POST['dname']
        telno = request.POST['telno']
        gender = request.POST['gender']
        dio = request.POST['diognosis']
        page = request.POST['page']
        email = request.POST['email']
        amb = request.POST['amb']
        try:
            diognosis = Diognosis.objects.get(id=id)
        except Exception, e:
            pass
        if diognosis:
	        diognosis.id=id
	        diognosis.dname=dname
	        diognosis.telno=telno
	        diognosis.gender=gender
	        diognosis.diognosis=dio
	        diognosis.page=page
	        diognosis.email=email
	        diognosis.amb=amb
	        diognosis.save()
	        editd_response = True
	        diog = Diognosis.objects.all().order_by('-id')
	        return render_to_response('Doct/doctorH.html', {'editd_response': editd_response, 'diog': diog}, context)

    else:
    	pass

	return render_to_response('Doct/doctorH.html', {'editd_response': editd_response}, context)
@login_required
def restricted(request):

	context=RequestContext(request)



	return render_to_response('Doct/restricted.html', { 'note': 'Wow you are already logged in' }, context)



def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)


	# Take the user back to the homepage.
	return HttpResponseRedirect('/Doct/')





