from django.conf.urls import url

import views

urlpatterns = [
	 url(r'^$', views.index, name='index'),
	 url(r'^graph/', views.formatData, name='test'),
	 url(r'^result/', views.newPlot, name='img'),
	 url(r'^chart/', views.subscribe, name='chart'),
	 url(r'^config/', views.config, name='config'),
]
