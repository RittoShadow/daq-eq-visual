from django.conf.urls import url

import views

urlpatterns = [
	 url(r'^$', views.home, name='home'),
	 url(r'^login/$', views.loginDAQEQ, name='login'),
	 url(r'^logout/$', views.logoutDAQEQ, name='logout'),
	 url(r'^graph/', views.index, name='test'),
	 url(r'^result/', views.formatData, name='result'),
	 url(r'^image/(?P<data>.+)', views.newPlot, name='img'),
	 url(r'^chart/', views.subscribe, name='chart'),
	 url(r'^config/', views.ConfigurationFormView.as_view(), name='config'),
	#  url(r'^config/', views.ConfigurationFormView, name='config'),
	 url(r'^notification/', views.NotificationFormView.as_view(), name='notify'),
	 url(r'^signal/', views.start_stop_signal, name='signal'),
	 url(r'^views/', views.view, name="view"),
	 url(r'^verify_config/', views.configVerification, name="verify"),
	 url(r'^verify_notification/', views.notificationVerification, name="verify"),
	 url(r'^sensors/', views.sensor, name="sensor"),
	 url(r'^script_configuration/', views.scriptConfiguration, name="scripts"),
]

#\[(\[(\-?(\d+\.\d+)+(e(\+|\-)\d+)?)(\-?(\d+\.\d+)+(e(\+|\-)\d+)?\,\s)+(\-?(\d+\.\d+)+(e(\+|\-)\d+)?)\](\,\s)?)+\]
