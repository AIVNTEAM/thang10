from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Question, Choice
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
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'temp1/results.html', {'question':question})

def votes(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		# selectedchoice = question.choice_set.get(pk=request.POST['choice'])
		selectedchoice = question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		return render(request, 'temp1/details.html', {
				'question':question,
				'error_message':"Ban chua chon dap an nao"
			})
	else:
		selectedchoice.votes += 1
		selectedchoice.save()
	# đối tượng HttpResponseRedirect
	# tránh các trường hợp người dùng nhấn nút back trên trình duyệt 
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))