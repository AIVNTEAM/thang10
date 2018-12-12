from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth import login, authenticate
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
								  UpdateView)
from django.db.models import Avg, Count
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import inlineformset_factory

from .models import User, Quiz, Question, Answer, TakenQuiz, Student
from .forms import (StudentSignupForm, 
	TeacherSignupForm, 
	QuestionForm,
	BaseAnswerInlineFormSet,
	StudentInterestsForm,
	TakeQuizForm)


from django.views.generic import TemplateView

# class HomeView(TemplateView):
# 	template_name = 'classroom/home.html'
def home(request):	
	if request.user.is_authenticated():
		if request.user.is_teacher:
			return redirect('quiz_change_list')
		else:
			return redirect('quiz_list')
	return render(request, 'classroom/home.html')

class SignUpView(TemplateView):
	template_name = 'registration/signup.html'

# Create your views here.
class StudentSignUpView(CreateView):
	model = User
	form_class = StudentSignupForm
	success_url = reverse_lazy('home')
	template_name = 'registration/signup_form.html'

	# du lieu co duoc truoc khi goi ra template them
	# du lieu lien quan den user_type => student
	def get_context_data(self, **kwargs):
		context = super(StudentSignUpView, self).get_context_data(**kwargs)
		context['user_type'] = 'student'
		return context

	def form_valid(self, form):
		result = super(StudentSignUpView, self).form_valid(form)
		cd = form.cleaned_data
		#xac thuc truoc khi goi login
		user = authenticate(username = cd['username'],
			password = cd['password1'])
		# user = form.save()
		login(self.request, user)		
		return result

class TeacherSignUpView(CreateView):
	model = User    #model tuong tac
	form_class = TeacherSignupForm         #form su dung cho view
	success_url = reverse_lazy('home')     #sau khi xu ly thanh cong
	template_name = 'registration/signup_form.html'   #template su dung

	def get_context_data(self, **kwargs):    #dua bien: user_type ra template
		context = super(TeacherSignUpView, self).get_context_data(**kwargs)
		context['user_type'] = 'teacher'
		return context

	def form_valid(self, form):
		result = super(TeacherSignUpView, self).form_valid(form)
		cd = form.cleaned_data
		#xac thuc truoc khi goi login
		user = authenticate(username = cd['username'],
			password = cd['password1'])
		# user = form.save()
		login(self.request, user)		
		return result
		
class QuizListView(ListView):
	model = Quiz
	ordering = ('name', )
	context_object_name = 'quizzes'
	template_name = 'classroom/teachers/quiz_change_list.html'

	def get_queryset(self):
		queryset = self.request.user.quizzes \
			.select_related('subject') \
			.annotate(question_count=Count('questions', distinct=True)) \
			.annotate(taken_count=Count('taken_quizzes', distinct=True))
		return queryset

class QuizCreateView(CreateView):
	model = Quiz
	fields = ('name', 'subject')  #hoac dung form_class neu co form class
	template_name = 'classroom/teachers/quiz_add_form.html'
	success_url = reverse_lazy('quiz_change_list')

	def form_valid(self, form):
		quiz = form.save(commit = False)
		quiz.owner = self.request.user
		quiz.save()
		return super(QuizCreateView, self).form_valid(form)

	# def get_success_url(self):
	# 	return reverse('quiz_change', kwargs={'pk': self.object.pk})

class QuizUpdateView(UpdateView):
	model = Quiz
	fields = ('name', 'subject', )
	context_object_name = 'quiz'	#goi ra view bien ten quiz
	template_name = 'classroom/teachers/quiz_change_form.html'
	# success_url = reverse_lazy('quiz_change_list')
	
	def get_context_data(self, **kwargs):
		context = super(QuizUpdateView, self).get_context_data(**kwargs)
		context['questions'] = self.get_object().questions \
			.annotate(answers_count=Count('answers'))
		return context

	def get_queryset(self):
		return self.request.user.quizzes.all()

	def get_success_url(self):
		return reverse('quiz_change', kwargs={'pk': self.object.pk})

class QuizDeleteView(DeleteView):
	model = Quiz
	context_object_name = 'quiz'
	template_name = 'classroom/teachers/quiz_delete_confirm.html'
	success_url = reverse_lazy('quiz_change_list')

	def delete(self, request, *args, **kqargs):
		quiz = self.get_object()
		return super(QuizDeleteView, self).delete(request, *args, **kwargs)

	def get_queryset(self):
		return self.request.user.quizzes.all()

class QuizResultsView(DetailView):
	model = Quiz
	context_object_name = 'quiz'
	template_name = 'classroom/teachers/quiz_results.html'

	def get_context_data(self, **kwargs):		
		quiz = self.get_object()
		taken_quizzes = quiz.taken_quizzes() \
						.select_related('student__user') \
						.order_by('-date')
		total_take_quizzes = taken_quizzes.count()
		quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
		extra_context = {
			'taken_quizzes': taken_quizzes,
			'total_take_quizzes': total_take_quizzes,
			'quiz_score': quiz_score
		}
		kwargs.update(extra_context)
		context = super(QuizResultView, self).get_context_data(**kwargs)
		return context

	def get_queryset(self):
		return self.request.user.quizzes.all()

def question_add(request, pk):
	# By filtering the quiz by the url keyword argument `pk` and
	# by the owner, which is the logged in user, we are protecting
	# this view at the object-level. Meaning only the owner of
	# quiz will be able to add questions to it.
	quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

	if (request.method == 'POST'):
		form = QuestionForm(request.POST)
		if form.is_valid():
			ques = form.save(commit=False)
			ques.quiz = quiz
			ques.save()
		return redirect('question_change', quiz.pk, ques.pk)
	else:
		form = QuestionForm()
	return render(request, 'classroom/teachers/question_add_form.html', 
		{'form': form, 'quiz': quiz})

def question_change(request, quiz_pk, question_pk):
	# Simlar to the `question_add` view, this view is also managing
	# the permissions at object-level. By querying both `quiz` and
	# `question` we are making sure only the owner of the quiz can
	# change its details and also only questions that belongs to this
	# specific quiz can be changed via this url (in cases where the
	# user might have forged/player with the url params.
	quiz = get_object_or_404(Quiz, pk = quiz_pk, owner = request.user)
	ques = get_object_or_404(Question, pk = question_pk, quiz=quiz)

	AnswerFormset = inlineformset_factory(
			Question, #parent model
			Answer, #base model
			formset = BaseAnswerInlineFormSet,
			fields = ('text', 'is_correct',),
			min_num = 2,
			validate_min = True,
			max_num = 10,
			validate_max = 10
		)

	if request.method == 'POST':
		form = QuestionForm(request.POST, instance=ques)
		formset = AnswerFormset(request.POST, instance=ques)
		if form.is_valid() and formset.is_valid():
			form.save()
			formset.save()
			return redirect('quiz_change', quiz.pk)
	else:
		form = QuestionForm(instance=ques)
		formset = AnswerFormset(instance=ques)
	
	return render(request, 'classroom/teachers/question_change_form.html', 
			{
				'quiz': quiz,
				'question': ques,
				'form': form,
				'formset': formset
			})

class QuestionDeleteView(DeleteView):
	model = Question
	context_object_name = 'question'
	template_name = 'classroom/teachers/question_delete_confirm.html'
	#vi url co dang 
	#^teacher/quiz/<int:quiz_pk>/question/<int:question_pk>/delete/
	#de lay id ta su dung: pk_url_kwarg de chi noi can lay id
	pk_url_kwarg = 'question_pk'

	def get_context_data(self, **kwargs):
		context = super(QuestionDeleteView, self).get_context_data(**kwargs)
		question = self.get_object()
		context['quiz'] = question.quiz
		return context

	def delete(self, request, *args, **kwargs):
		question = self.get_object()	
		return super(QuestionDeleteView, self).delete(*args, **kqargs)

	def get_queryset(self):
		return Question.objects.filter(quiz__owner=self.request.user)

	def get_success_url(self):
		question = self.get_object()
		return reverse('quiz_change', 
			kwargs={'pk': question.quiz_id})


class StudentQuizListView(ListView):
	model = Quiz
	ordering = ('name', )
	context_object_name = 'quizzes'
	template_name = 'classroom/students/quiz_list.html'

	def get_queryset(self):
		student = self.request.user.student  #1-to-1: User - Student
		#lay ds mon hoc ma student quan tam
		student_interests = student.interests.values_list('pk', flat=True)
		#lay ds quiz ma student da tham gia
		taken_quizzes = student.quizzes.values_list('pk', flat=True)
		result = Quiz.objects.filter(subject__in=student_interests)\
						.exclude(pk__in=taken_quizzes)\
						.annotate(questions_count = Count('questions'))\
						.filter(questions_count__gt=0)
		return result

class TakenQuizListView(ListView):
	model = TakenQuiz
	context_object_name = 'taken_quizzes'
	template_name = 'classroom/students/taken_quiz_list.html'

	def get_queryset(self):
		queryset = self.request.user.student.taken_quizzes \
					.select_related('quiz', 'quiz__subject') \
					.order_by('quiz__name')
		return queryset


class StudentInterestsView(ListView):
	model = Student
	form_class = StudentInterestsForm
	template_name = 'classroom/students/interests_form.html'
	success_url = reverse_lazy('quiz_list')

	def get_object(self):
		return self.request.user.student   #truy qua user -> student: 1-1
	def form_valid(self, form):
		return super(StudentInterestsView, self).form_valid()

def take_quiz(request, quiz_pk):
	quiz = get_object_or_404(Quiz, pk=quiz_pk)
	student = request.user.student

	# if (student.quizzes.filter(pk=quiz_pk).exists()):
		# return render(request, 'students/taken_quiz.html')

	total_questions = quiz.questions.count()
	unanswered_questions = student.get_unanswered_questions(quiz)
	total_unanswered_questions = unanswered_questions.count()
	progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
	question = unanswered_questions.first()

	if request.method == 'POST':
		form = TakeQuizForm(question=question, data=request.POST)
		if form.is_valid():
			student_answer = form.save(commit = False)
			student_answer.student = student
			student_answer.save()
			if student.get_unanswered_questions(quiz).exists():
				return redirect('take_quiz', quiz_pk)
			else:
				correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
				score = round((correct_answers / total_questions) * 100.0, 2)
				TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
				if score < 50.0:
					messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
				else:
					messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
				return redirect('quiz_list')
	else:
		form = TakeQuizForm(question=question)

	return render(request, 'classroom/students/take_quiz_form.html', {
		'quiz': quiz,
		'question': question,
		'form': form,
		'progress': progress
	})