from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	response = HttpResponse()
	response.write("<h1>Welcome</h1>")
	response.write("This is the polls app")
	return response