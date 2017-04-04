

'''admin configurations'''
from django.contrib import admin
import doct_admin.views as remit_admin
from doct_admin  import  views as remit_admin
from django.conf.urls import *
from django.contrib.auth.models import User
import manDoct.settings as settings
from django.contrib.auth.models import Group
# remove defaults
admin.site.unregister(User)
admin.site.unregister(Group)

'''
register admin urls
'''


def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
        	url(r'^$', admin.site.admin_view(
                               remit_admin.home), name="admin_dashboard"),
        	 url(r'^logout/$', 'django.contrib.auth.views.logout',
                            {'next_page': settings.BASE_URL } , name="admin_logout"),
                          

                           )
        return my_urls + urls
    return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls


