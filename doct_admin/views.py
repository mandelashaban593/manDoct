# Create your views here.
from django.shortcuts import HttpResponse, render_to_response, \
    HttpResponseRedirect, render,get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from Doct.models import Page,Rate, UserProfile, Register,Profile, Topup,Register, Enterpay,Illness
from Doct.models import Diognosis,Conddrugs,Contact,converse,convMembers,convReg,convPersonFrien,Messages
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from doct_admin.forms import ChangeAdminTelephoneForm,ChangeAdminPassword,CreateAdminUserForm,EditAdminUserForm
from django.contrib.auth.models import User
from doct_admin.utils import debug
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import doct_admin.utils as admin_utils
from doct_admin.utils import log_action, store_login_info


def home(request):
	context = RequestContext(request)
	if request.user.is_superuser:
		return render_to_response('admin/index.html', {}, context)
	if request.user.is_staff:
		return render_to_response('admin/index_staff.html', {}, context)
	else:
	 	return HttpResponseRedirect('/')
	
    
    	

 

def user_login(request):
	# Like before, obtain the context for the user's hrequest.
	context = RequestContext(request)
	msg = ''
	response = None
	log = False
	convmem = ''
	phonedoctor = ''


	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		password = request.POST['password']
		username = request.POST['username']
		r = None	

		

		try:
			r = Register.objects.get(password=password, telno=username)
		except Exception, e:
			print "Invalid Username Or Password", e

		if r:
			if r.role=='patient':
				patlog=True
				return render_to_response('Doct/patientH.html', {'patlog':patlog}, context)
			elif r.role =='doctor':
				doctlog=True
				diog = Diognosis.objects.all()
				convmem = convMembers.objects.filter(phonedoctor=username)
				if convmem:
					phonedoctor=username
					print phonedoctor
				paginator = Paginator(diog, settings.PAGNATION_LIMIT)
				page = request.GET.get('page')
				try:
					diog = paginator.page(page)
				except PageNotAnInteger:
					diog = paginator.page(1)
					# If page is not an integer, deliver first page.
				except EmptyPage:
					# If page is out of range (e.g. 9999), deliver last page of results.
					diog = paginator.page(paginator.num_pages)
			        
			  
				return render_to_response('Doct/doctorH.html', {'diogs':diog, 'phonedoctor':phonedoctor,'doctlog':doctlog}, context)
			elif r.role =='admin':
				adlog = True
				return render_to_response('admin/index.html', {'adlog':adlog}, context)
				
			else:
				return render_to_response('admin/index_staff.html', {}, context)
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
		return render_to_response('Doct/login.html', {'log':log}, context)
    	

    	
def change_stuff_telephone(request, is_customer_care=False):
    '''create an admin user'''
    context = RequestContext(request)



    
    form = ''
    if request.POST:
        form = ChangeAdminTelephoneForm(request.POST)
        if form.is_valid():
        	try:
	        	reg = Register.objects.get(telno=request.POST['old_phone'])
	        	if reg:
	        		reg.telno = request.POST['new_phone']
	        		reg.save()
	        except Exception, e:
	        	print "Invalid Telphone number", e

           
			messages.success(request, "The User  Phone number Was Successfully Changed")
    super_admin = True
    return render_to_response('Doct/change_stuff_telephone.html', {'form': form, 'super_admin':super_admin},context)


def change_stuff_password(request, is_customer_care=False):
    '''create an admin user'''
    context = RequestContext(request)



    
    form = ''
    if request.POST:
        form = ChangeAdminPassword(request.POST)
        if form.is_valid():
        	try:
	        	reg = Register.objects.get(telno=request.POST['old_pass'])
	        	if reg:
	        		reg.password = request.POST['new_pass']
	        		reg.save()
	        except Exception, e:
	        	print "Invalid Password number", e

           
			messages.success(request, "The User Password Was Successfully Changed")
    super_admin = True
    return render_to_response('Doct/change_stuff_password.html', {'form': form, 'super_admin':super_admin},context)




def assign_permissions(user, form, update=False, is_customer_care=False):
    '''assign staff members permissions'''
    if user:

        if is_customer_care:
            # customer care options
            content_type = ContentType.objects.get_for_model(Transaction)
            view_transaction = Permission.objects.get(
                content_type=content_type, codename="view_transaction")
            edit_transactions = Permission.objects.get(
                content_type=content_type, codename="edit_transaction")
            user.user_permissions.add(view_transaction)
            user.user_permissions.remove(edit_transactions)

        else:
            content_type = ContentType.objects.get_for_model(Profile)
            view_profile = Permission.objects.get(
                content_type=content_type, codename="view_profile")
            edit_profile = Permission.objects.get(
                content_type=content_type, codename="edit_profile")
            if form.cleaned_data['users'] == '2':
                user.user_permissions.add(view_profile)
                user.user_permissions.remove(edit_profile)
            elif form.cleaned_data['users'] == '3':
                user.user_permissions.add(edit_profile, view_profile)
            if update and form.cleaned_data['users'] == '1':
                user.user_permissions.remove(edit_profile, view_profile)

            # rates edit permissions
            content_type = ContentType.objects.get_for_model(Rate)
            view_rate = Permission.objects.get(
                content_type=content_type, codename="view_rate")
            edit_rate = Permission.objects.get(
                content_type=content_type, codename="edit_rate")
            if form.cleaned_data['rates'] == '2':
                user.user_permissions.add(view_rate)
                user.user_permissions.remove(edit_rate)
            elif form.cleaned_data['rates'] == '3':
                user.user_permissions.add(view_rate, edit_rate)
            if update and form.cleaned_data['rates'] == '1':
                user.user_permissions.remove(edit_rate, view_rate)

            # transaction edit permissions
            content_type = ContentType.objects.get_for_model(Transaction)
            view_transaction = Permission.objects.get(
                content_type=content_type, codename="view_transaction")
            edit_transactions = Permission.objects.get(
                content_type=content_type, codename="edit_transaction")
            if form.cleaned_data['transactions'] == '2':
                user.user_permissions.add(view_transaction)
                user.user_permissions.remove(edit_transactions)
            elif form.cleaned_data['transactions'] == '3':
                user.user_permissions.add(view_transaction, edit_transactions)
            if update and form.cleaned_data['transactions'] == '1':
                user.user_permissions.remove(
                    edit_transactions, view_transaction)

            # reports
            content_type = ContentType.objects.get_for_model(Transaction)
            view_reports = Permission.objects.get(
                content_type=content_type,
                codename="view_reports"
            )
            if form.cleaned_data['reports'] == '2':
                user.user_permissions.add(view_reports)
            if update and form.cleaned_data['reports'] == '1':
                user.user_permissions.remove(view_reports)

            # audit trails
            content_type = ContentType.objects.get_for_model(AdminProfile)
            view_audit_trail = Permission.objects.get(
                content_type=content_type, codename="view_audit_trail")
            try:
                if form.cleaned_data['audit_trail'] == '2':
                    user.user_permissions.add(view_audit_trail)
                if update and form.cleaned_data['audit_trail'] == '1':
                    user.user_permissions.remove(view_audit_trail)
            except Exception, e:
                print e
            user.save()




def create_stuff_user(request, is_customer_care=False):
    '''create an admin user'''
    context = RequestContext(request)
    form = CreateAdminUserForm()
    if request.POST:
        form = CreateAdminUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.save()
            user.is_staff = True

            reg = Register(user=user,fname=request.POST['fname'], sname=request.POST['sname'],
            	page=request.POST['page'],gender=request.POST['gender'],telno=request.POST['telno'],
            	username=request.POST['username'],password=request.POST['password'],email=request.POST['email'],
            	street=request.POST['street'],specialty=request.POST['specialty'],profile_pic=request.POST['profile_pic'], role=request.POST['role'])
            reg.save()
      
            messages.success(request, "The User Was Successfully Created")
    super_admin = True
    return render_to_response('Doct/create_stuff_user.html', {'form': form, 'super_admin':super_admin},context)






def stuff_users(request, name=False):
    '''fetch stuff '''
    context = RequestContext(request)
    
    user_list = Register.objects.filter(role="doctor")  # (is_staff=True)
    debug(user_list, 'stuff')
    user_list = user_list.filter().order_by('-id')
    # search query
    if 'q' in request.GET:
        pretitle += ' | %s' % request.GET['q']
        page_title += ' | %s' % request.GET['q']
        user_list = user_list.filter(
            Q(username__icontains='' + request.GET['q'] + ''))
    paginator = Paginator(user_list, settings.PAGNATION_LIMIT)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)

    super_admin = True
    return render_to_response('Doct/stuff_users.html', {'users': users, 'super_admin':super_admin},context)




def patients(request, name=''):
    '''
    @request  request object
    '''
    # user_list = Profile.objects.filter(account_verified=True,user__isnull=False)
    # print name
    context = RequestContext(request)
    pretitle = 'verified users'
    page_title = 'verified users'
    admin= True
    super_admin= True

    user_list = Illness.objects.all()
    
    if name == 'blocked':
        pretitle = 'Blocked Users'
        page_title = 'Blocked Users'
        user_list = admin_utils.blocked_users()
    elif name == 'top':
        pretitle = 'Blocked Users'
        page_title = 'Blocked Users'
        user_list = Illness.objects.all()
    elif name == 'search':
        pretitle = 'User Search'
        page_title = 'User Search'
        user_list = Illness.objects.filter()
    else:
        print "Nothing"
      

    user_list = user_list.filter().order_by('-id')
    # search query
    if 'q' in request.GET:
        pretitle += ' | %s' % request.GET['q']
        page_title += ' | %s' % request.GET['q']
        user_list = user_list.filter(
            Q(pname__icontains='' + request.GET['q'] + '') | Q(sname__icontains='' + request.GET['q'] + ''))

    paginator = Paginator(user_list, settings.PAGNATION_LIMIT)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        users = paginator.page(paginator.num_pages)
    log_action(request, model_object=user_list,
               action_flag=13, change_message='searched user')
    return render_to_response('Doct/users.html', {'users': users, 'super_admin':super_admin,'admin':admin},context)




def edit_stuff_user(request, name):
    id = int(name)
    context = RequestContext(request)
    users = ''
    post_values = {}
    user = get_object_or_404(Register.objects.filter(id=id))
    form = EditAdminUserForm()
    post_values = request.POST.copy()
    fname = request.POST['fname']
    sname = request.POST['sname']
    page = request.POST['page']
    gender = request.POST['gender']
    email = request.POST['email']
    username = request.POST['username']
    street = request.POST['street']
    specialty = request.POST['specialty']
    profile_pic = request.POST['profile_pic']
    role = request.POST['role']
    if request.POST:
        form = EditAdminUserForm(request.POST)
        if form.is_valid():
            user.fname = fname
            user.sname = sname
            user.page = page
            user.gender = gender
            user.email = email
            user.username = username
            user.street = street
            user.specialty = specialty
            user.profile_pic = profile_pic
            user.role = role
            user.save()

            messages.success(request, "The Stuff User Was Successfully Edited")
    super_admin = True
    return render_to_response('Doct/edit_stuff_user.html', {'stuff_profile': user, 'super_admin':super_admin},context)





def dashboard(request):
    context = RequestContext(request)

    doctlog=True
    diog = Diognosis.objects.all().order_by("-id")

    paginator = Paginator(diog, settings.PAGNATION_LIMIT)
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
        
  
    return render_to_response('Doct/index_staff.html', {'diogs':diog,'staf':staf, 'doctlog':doctlog}, context)



def dashboard2(request):
    context = RequestContext(request)

    doctlog=True
    diog = Illness.objects.all().order_by("-id")
    diog_count = Illness.objects.all().order_by("-id").count()
    undiog_count = Diognosis.objects.filter(gender='0').count()
    doctor_count = Register.objects.filter(role='doctor').count()
    


    paginator = Paginator(diog, settings.PAGNATION_LIMIT)
    page = request.GET.get('page')
    try:
        diog = paginator.page(page)
    except PageNotAnInteger:
        diog = paginator.page(1)
        # If page is not an integer, deliver first page.
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        diog = paginator.page(paginator.num_pages)

    
    super_admin = True
        
  
    return render_to_response('Doct/index_admin.html', {'diogs':diog,'super_admin':super_admin, 'doctlog':doctlog,'diog_count':diog_count,'undiog_count':undiog_count,'doctor_count':doctor_count}, context)


