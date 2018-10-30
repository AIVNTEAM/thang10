from django.db import models
from django.shortcuts import  render
from django.http import HttpResponse
from .forms import UploadFilesForm

# Create your tests here.
def fileUploaderView(request):
	if request.method == "POST":
		form = UploadFilesForm(request.POST, request.FILES)
		if(form.is_valid()):
			upload(request.FILES['file'])
			return HttpResponse("<h2>Upload file thanh cong</h2>")
		else:
			return HttpResponse("<h2>Upload that bai</h2>")
	form = UploadFilesForm()
	return render(request, 'fileUploaderTemplate.html', {'form': form})
def upload(f):
	file = open(f.name, 'wb+')
	# copy vao thu muc cua server - co file manage.py
	for chunk in f.chunks():
		file.write(chunk)