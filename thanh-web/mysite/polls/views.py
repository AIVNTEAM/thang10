from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Question
# Create your views here.
def index(request):
	# response = HttpResponse()
	# response.write("<h1>Welcome</h1>")
	# response.write("This is the polls app")
	# return response
	lasted_question_list = Question.objects.order_by('-pub_date')[:5]
	# output = ','.join([q.question_text for q in lasted_question_list])
	context = {
		'lasted_question_list': lasted_question_list
	}
	return render(request, 'temp1/index.html', context)
def detail(request, question_id):
	# return HttpResponse("Detail for question %s" %question_id)
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404("Question does not existe")
	return render(request, 'temp1/details.html', {'question':question})
def results(request, question_id):
	return HttpResponse("results of question %s" %question_id)
def votes(request, question_id):
	return HttpResponse("votes on question %s" % question_id)