from django.conf.urls import patterns, url
from Doct import views
from django.conf.urls import patterns, url
from Doct import views
urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		#url(r'^about/$', views.about, name='about'),
		url(r'^add_category/$', views.add_category, name='add_category'), #NEW MAPPING!
		url(r'^add_page/$', views.add_page, name='add_page'),

		url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
		url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
		url(r'^register/$', views.p_reg, name='register'),
		url(r'^send_at/$', views.send_at, name='send_at'),
		url(r'^airtime_sent_details/$', views.airtime_sent_details, name='airtime_sent_details'),
		
		url(r'^login/$', views.user_login, name='login'),
		url(r'^authConsult/$', views.authConsult, name='authConsult'),
		url(r'^authdiog/$', views.authdiog, name='authdiog'),
		url(r'^illness/$', views.illness, name='illness'),
		url(r'^view_illness/$', views.view_illness, name='view_illness'),
		url(r'^view_illness2/$', views.view_illness2, name='view_illness2'),
	
		url(r'^delP/$', views.delP, name='delP'),
		url(r'^patientD/$', views.patientD, name='patientD'),
		url(r'^doctorD/$', views.doctorD, name='doctorD'),
		url(r'^patientH/$', views.patientH, name='patientH'),
		url(r'^doctorH/$', views.doctorH, name='doctorH'),
		url(r'^diognosis/$', views.diognosis, name='diognosis'),
		url(r'^diogform/$', views.diogform, name='diogform'),
		url(r'^view_diognosis/$', views.view_diognosis, name='view_diognosis'),
		url(r'^authindillness/$', views.authindillness, name='authindillness'),
		url(r'^ind_illness/$', views.ind_illness, name='ind_illness'),
		url(r'^admin_pat/$', views.admin_pat, name='admin_pat'),
		url(r'^admin_doct/$', views.admin_doct, name='admin_doct'),
		url(r'^adminH/$', views.adminH, name='adminH'),
		url(r'^receipt/$', views.receipt, name='receipt'),
		url(r'^index_receipt/$', views.index_receipt, name='index_receipt'),
		url(r'^doctor_receipt/$', views.doctor_receipt, name='doctor_receipt'),
		url(r'^about/$', views.about, name='about'),
		url(r'^contact/$', views.contact, name='contact'),
		url(r'^regdoctor/$', views.regdoctor, name='regdoctor'),
		url(r'^enterpay/$', views.enterpay, name='enterpay'),
		url(r'^restricted/', views.restricted, name='restricted'),
		url(r'^signout/$', views.user_logout, name='logout'),
		url(r'^editdiog/(?P<diog_id>\d+)/$', views.editdiog, name='editdiog'),
		url(r'^edited_diog/$', views.edited_diog, name='edited_diog'),
		url(r'^user_log/$', views.user_log, name='user_log'),
		url(r'^AddIllDet/$', views.AddIllDet, name='AddIllDet'),
		
	
	
		)  # New!


