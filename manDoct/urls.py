from django.conf.urls import patterns, include, url
from django.conf import settings
from Doct import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin # UNCOMMENT THIS LINE
admin.autodiscover() # UNCOMMENT THIS LINE, TOO!
urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^Doct/', include('Doct.urls')),
		url(r'^admin/', admin.site.urls), # ADD THIS LINE
)
if settings.DEBUG:
		urlpatterns += patterns(
				'django.views.static',
				(r'media/(?P<path>.*)',
				'serve',
				{'document_root': settings.MEDIA_ROOT}), )