from django.conf.urls import patterns, url
from Doct import views
from doct_admin import views as doct_views
from django.conf.urls import patterns, url,include
from django.contrib import admin
admin.autodiscover()

from Doct import views
urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		#url(r'^about/$', views.about, name='about'),

		
		url(r'^add_page/$', views.add_page, name='add_page'),
		
		url(r'^register/$', views.register, name='register'),
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
		url(r'^whyus/$', views.whyus, name='whyus'),
		url(r'^about/$', views.about, name='about'),
		url(r'^contact/$', views.contact, name='contact'),
		url(r'^regdoctor/$', views.regdoctor, name='regdoctor'),
		url(r'^enterpay/$', views.enterpay2, name='enterpay'),
		url(r'^restricted/', views.restricted, name='restricted'),
		url(r'^signout/$', views.user_logout, name='logout'),
		url(r'^editdiog/(?P<diog_id>\d+)/(?P<ill_id>\d+)/$', views.editdiog, name='editdiog'),
		url(r'^edited_diog/$', views.edited_diog, name='edited_diog'),
		url(r'^user_log/$', views.user_log, name='user_log'),
		url(r'^AddIllDet/$', views.AddIllDet, name='AddIllDet'),
		url(r'^how_it_works/$', views.how_it_works, name='how_it_works'),
		url(r'^team/$', views.our_team, name='team'),
		url(r'^follup/$', views.follup, name='follup'),
		url(r'^repmsg/$', views.repmsg, name='repmsg'),

		url(r'^sendmessage/$', views.sendmessage, name='sendmessage'),
		url(r'^converse/$', views.patientConverse, name='converse'),

		url(r'^doctConv/$', views.doctConv, name='doctConv'),

		url(r'^sendtext/$', views.Converse, name='sendtext'),
		url(r'^dviewmsg/$', views.dviewmsg, name='dviewmsg'),
		url(r'^sendrep/$', views.sendrep, name='sendrep'),
		url(r'^convbaddy/$', views.convbaddy, name='convbaddy'),
		url(r'^searchphone/$', views.searchPhone, name='searchphone'),
		url(r'^convtext/$', views.convtext, name='convtext'),
		url(r'^sendtext1/$', views.Converse1, name='sendtext1'),
		url(r'^chuck/', include(
                           admin.site.urls)),

		url(r'^addadmin/$', 'doct_admin.views.change_stuff_telephone', name="create_admin_telephone"),
		url(r'^editpass/$', 'doct_admin.views.change_stuff_password', name="create_admin_telephone"),
		url(r'^addstuff/$', 'doct_admin.views.create_stuff_user', name="create_admin_user"),
		 url(r'^users/stuffs/$','doct_admin.views.stuff_users', name="view_admin_user"),
		 url(r'^404$', views.custom_404, name='custom_404'),
		url(r'^users/patients/$','doct_admin.views.patients', name="view_patient_user"),
		url(r'^edit/stuffs/(\w+)/$','doct_admin.views.edit_stuff_user', name="edit_admin_user"),

		url(r'^ajconv_list/$',
                           'Doct.views.ajconv_list', name='ajconv_list'),
		url(r'^ajDoctconv_list/$',
                           'Doct.views.ajDoctconv_list', name='ajDoctconv_list'),

		url(r'^ambulance/$', views.ambulance, name='ambulance'),
		url(r'^orderdrugs/$', views.orderdrugs, name='orderdrugs'),
		url(r'^labtests/$', views.labtests, name='labtests'),

		url(r'^addcontact/$', views.addcontact, name='addcontact'),

		url(r'^dashboard/$', 'doct_admin.views.dashboard', name='dashboard'),
		url(r'^dashboard2/$', 'doct_admin.views.dashboard2', name='dashboard2'),
		url(r'^test/$', 'Doct.views.test', name='test'),
		url(r'^logout/$', views.user_logout, name='logout'),
		

		)  # New!
