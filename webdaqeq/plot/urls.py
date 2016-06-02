from django.conf.urls import url

import views

urlpatterns = [
	 url(r'^$', views.home, name='home'),
	 url(r'^graph/', views.index, name='test'),
	 url(r'^result/', views.formatData, name='img'),
	 url(r'^image$', views.newPlot, name='plot'),
	 url(r'^chart/', views.subscribe, name='chart'),
	 url(r'^config/', views.ConfigurationFormView.as_view(), name='config'),
	 url(r'^notification/', views.NotificationFormView.as_view(), name='notify'),
]
