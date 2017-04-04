
from django.contrib.contenttypes.models import ContentType

from django.conf import settings
from Doct.models import Profile
from doct_admin.forms import LoginInfoForm, UserActionsForm, LogEntryForm


def users_pending_verification(count=False):
    '''get pending users'''
    user_list = Profile.objects.filter(
        account_verified=False, id_verified=False, account_blocked=False, phone_verified=True)
    if count:
        user_list = user_list.count()
    return user_list


def verified_users(count=False):
    '''get pending users'''
    user_list = Profile.objects.filter(
        account_verified=True, id_verified=True, account_blocked=False,
        user__isnull=False)
    if count:
        user_list = user_list.count()
    return user_list


def unverified_users(count=False):
    '''get pending users'''
    user_list = Profile.objects.filter(id_pic='',account_verified=False, id_verified=False, account_blocked=False,user__isnull=False)
    if count:
        user_list = user_list.count()
    return user_list


def blocked_users(count=False):
    '''get pending users'''
    user_list = Profile.objects.filter(
        account_blocked=True)
    if count:
        user_list = user_list.count()
    return user_list



def store_login_info(request):
    '''store login information'''
    try:
        meta = request.META.copy()
        data = {'user_agent':meta.pop('HTTP_USER_AGENT', None)}
        data['remote_addr'] = meta.pop('REMOTE_ADDR', None)
        data['user'] = request.user.pk
        form = LoginInfoForm(data)
        if form.is_valid():
            obj = form.save()
            request.session['login_info'] = obj.pk
        else:
            debug(form.errors,'Session Info Save')
    except Exception, e:
        debug(e,'Session Info Save')
    log_action(request, model_object=request.user, action_flag=10, change_message='Logged In')


def log_action(request, model_object, action_flag, change_message=''):
    '''log user actions'''

    logdata = {}
    path = request.get_full_path()
    change_message = '%s via <a href="%s">%s</a> ' % (change_message, path, path )
    try:
        logdata['user'] = request.user.id
        logdata['action_flag'] = action_flag
        logdata['change_message'] = change_message
        logdata['object_repr'] = unicode(model_object)[:200]
    except Exception, e:
        debug(e,'logdata error')
        pass


    try:
        logdata['content_type'] = ContentType.objects.get_for_model(model_object).pk
        logdata['object_id'] = model_object.id
    except Exception, e:
        debug(e,'logdata save error')
        pass
    

    logform = LogEntryForm(logdata)
    if logform.is_valid():
        obj = logform.save()        
        try:
            data = {'log_entry':obj.pk, 'user':request.user.pk}
            if not 'login_info' in request.session:
                store_login_info(request)
            data['session'] = request.session['login_info']
            form = UserActionsForm(data)
            if form.is_valid():
                form.save()
            else:
                debug(form.errors,'Log Action Save')
        except Exception, e:
            debug(e, 'Log Action Save')
    else:
        debug(logform.errors,'Log Action Save errors')
        #pass
    





def debug(e, txt=False, log='debug'):
    if settings.LOCALHOST:
        if not txt:
            txt = ''
        print >> sys.stderr, 'Debuging____________________ %s' % txt
        print >> sys.stderr, e
    else:
        try:
            old_stdout = sys.stdout
            log_file = open("%slogs/%s.log" % (settings.BASE_DIR, log), "a")
            sys.stdout = log_file
            print '%s: Debuging____________________ %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                           txt)
            print e
            sys.stdout = old_stdout
            log_file.close()
        except Exception, e:
            pass
