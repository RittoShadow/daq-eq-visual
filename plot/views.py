from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("This is not the greatest page in the world. \nThid is just an index.")
# Create your views here.

def formatData(request):
	return None
