'''
Decorators
'''
from django.shortcuts import HttpResponseRedirect, get_object_or_404
import manDoct.settings as settings
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse


def logged_out_required(function):
    '''This page cannot be viewed if a user is logged'''
    def wrapper(request, *args, **kw):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        else:
            return function(request, *args, **kw)
    return wrapper


def login_required(function):
    '''This page cannot be viewed if a user is logged out '''
    def wrapper(request, *args, **kw):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))
        else:
            # admins go to back admin page
            if request.user.is_staff or request.user.is_superuser:
                return HttpResponseRedirect(reverse('admin:admin_dashboard'))
            return function(request, *args, **kw)
    return wrapper


def admin_required(function):
    '''This page cannot be viewed if a user is not stuff'''
    def wrapper(request, *args, **kw):
        if request.user.is_active and request.user.is_staff:
            return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(reverse('custom_404'))
    return wrapper


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            # return HttpResponseBadRequest()
            return HttpResponseRedirect(reverse('custom_404'))
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
