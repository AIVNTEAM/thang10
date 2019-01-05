from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from .models import Course, Module, Content
from .forms import ModuleFormSet, StudentSignupForm, TeacherSignupForm
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from .models import User, Subject, Teacher
from students.forms import CourseEnrollForm
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate

# Sau khi dang nhap - dua vao role de chuyen huong
def home(request):	
	if request.user.is_authenticated():
		if request.user.is_teacher:
			return redirect('manage_course_list')
		else:
			return redirect('student_course_list')
	return render(request, 'home/home.html')

class HomeView(TemplateView):
	template_name = 'home/home.html'

#mixins
class OwnerMixin(object):
	def get_queryset(self):
		qs = super(OwnerMixin, self).get_queryset()
		#retrieve objects that belong to the current user
		# return qs.filter(owner = self.request.user)
		#04/01/2019: CongThanh: get objects lien quan den giao vien tao
		#teacher - user quan he 1 - 1
		return qs.filter(owner = self.request.user.teacher)

class OwnerEditMixin(object):
	def form_valid(self, form):
		#automatically set the current user in the 
		#owner attribute of the object being saved
		form.instance.owner = self.request.user.teacher
		return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin):
	model = Course

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
	fields = ['subject', 'title', 'slug', 'overview']
	#redirect the user after the form is successfully submitted.
	success_url = reverse_lazy('manage_course_list')
	template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):	
	template_name = 'courses/manage/course/list.html'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
	pass

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
	pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
	template_name = 'courses/manage/course/delete.html'
	success_url = reverse_lazy('manage_course_list')	

#lien quan toi Module
#TemplateResponseMixin: This mixin takes charge of rendering templates
#and returning an HTTP response. It requires a template_name attribute
#that indicates the template to be rendered and provides the render_to_
#response() method to pass it a context and render the template.
class CourseModuleUpdateView(TemplateResponseMixin, View):
	template_name = 'courses/manage/module/formset.html'
	course = None
	#define this method to avoid repeating the code to build
	#the formset. We create a ModuleFormSet object for the given Course object
	#with optional data.
	def get_formset(self, data=None):
		return ModuleFormSet(instance=self.course, data=data)

	# This method is provided by the View class. It takes an HTTP
	# request and its parameters and attempts to delegate to a lowercase method
	# that matches the HTTP method used: A GET request is delegated to the
	# get() method and a POST request to post() respectively. In this method,
	# we use the get_object_or_404() shortcut function to get the Course object
	# for the given id parameter that belongs to the current user. We include this
	# code in the dispatch() method because we need to retrieve the course for
	# both GET and POST requests. We save it into the course attribute of the
	# view to make it accessible to other methods.
	# Hàm view được trả về bởi as_view sẽ là phần được sử dụng của 
	# mọi class-based View. Khi được gọi, công việc của nó là 
	# sử dụng dispatch để xử lý truy vấn 
	# từ người dùng và gọi đến các hàm xử lý tương ứng.
	def dispatch(self, request, pk):
		self.course = get_object_or_404(Course, 
			id=pk, owner=request.user.teacher)
		return super(CourseModuleUpdateView, self).dispatch(request, pk)
	#Executed for GET requests. We build an empty ModuleFormSet
	#formset and render it to the template together with the current
	#Course object using the render_to_response() method provided by
	#TemplateResponseMixin.
	def get(self, request, *args, **kwargs):
		formset = self.get_formset()
		return self.render_to_response({'course': self.course,
										'formset': formset})

	# Executed for POST requests. In this method, we perform the
	# following actions:
	# 1. We build a ModuleFormSet instance using the submitted data.
	# 2. We execute the is_valid() method of the formset to validate all
	# of its forms.
	# 3. If the formset is valid, we save it by calling the save() method. At
	# this point, any changes made, such as adding, updating, or marking
	# modules for deletion, are applied to the database. Then, we redirect
	# users to the manage_course_list URL. If the formset is not valid, we
	# render the template to display any errors instead.
	def post(self, request, *args, **kwargs):
		formset = self.get_formset(data=request.POST)
		if (formset.is_valid()):
			formset.save()
			return redirect('manage_course_list')
		return self.render_to_response({'course': self.courses,
										'formset': formset})
#allow us to create and
#update contents of different models
class ContentCreateUpdateView(TemplateResponseMixin, View):
	module = None
	model = None
	obj = None	#neu cap nhat thi obj la obj cap nhat, con them moi la None
	template_name = 'courses/manage/content/form.html'

	def get_model(self, model_name):
		if model_name in ['text', 'video', 'image', 'file']:
			return apps.get_model(app_label='courses', model_name=model_name)
		return None

	#build a dynamic form using the modelform_factory()
	def get_form(self, model, *args, **kwargs):
		Form = modelform_factory(model, 
						exclude=['owner', 'order', 'created', 'updated'])
		return Form(*args, **kwargs)
	#receives the following URL parameters and stores the
	#corresponding module, model, and content object as class attributes:
	def dispatch(self, request, module_id, model_name, id=None):
		self.module = get_object_or_404(Module, id=module_id, 
						course__owner=request.user.teacher)
		self.model = self.get_model(model_name)
		#id: The id of the object that is being updated. 
		#It's None to create new objects.
		if id:
			self.obj = get_object_or_404(self.model, id=id, owner=request.user)
		return super(ContentCreateUpdateView, self).dispatch(request, module_id, model_name, id)

	def get(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model, instance=self.obj)
		return self.render_to_response({'form': form, 'object': self.obj})

	def post(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model,
							instance=self.obj,
							data=request.POST,
							files=request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.owner = request.user.teacher
			obj.save()
			if not id:
				#new content
				Content.objects.create(module=self.module,
					item=obj)
			return redirect('module_content_list', self.module.id)
		return self.render_to_response({'form': form, 'object': self.obj})

class ContentDeleteView(View):

	def post(self, request, id):
		content = get_object_or_404(Content, id=id,
			module__course__owner=request.user)
		module = content.module #lay module de co id sau do redirect o lenh cuoi
		#it deletes the related Text, Video, Image, or File object
		content.item.delete()
		content.delete()  #delete content
		return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
	template_name = 'courses/manage/module/content_list.html'

	def get(self, request, module_id):
		module = get_object_or_404(Module, id=module_id, 
			course__owner=request.user.teacher)
		return self.render_to_response({'module': module})

#view cap nhat thu tu module dung AJAX
# CsrfExemptMixin: To avoid checking for a CSRF token in POST requests.
# We need this to perform AJAX POST requests without having to generate
# csrf_token.
# JsonRequestResponseMixin: Parses the request data as JSON
class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Module.objects.filter(id=id, course__owner=request.user.teacher).update(order=order)
		return self.render_json_response({'saved': 'OK'})

#order content - tuong tu nhu tren
class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Content.objects.filter(id=id, module__course__owner=request.user.teacher).update(order=order)
		return self.render_json_response({'saved': 'OK'})

# Published
# Displaying courses 
class CourseListView(TemplateResponseMixin, View):
	model = Course
	template_name = 'courses/course/list.html'
	def get(self, request, subject=None):
		#subjects them truong: total_course = cach thong qua thuoc tinh courses
		subjects = Subject.objects.annotate(total_course = Count('courses'))
		#module them truong: total_module => dua thuoc tinh modules
		courses = Course.objects.annotate(total_module = Count('modules'))

		if subject:
			subject = get_object_or_404(Subject, slug=subject)
			courses = courses.filter(subject=subject)

		return self.render_to_response({'subjects': subjects,
										'subject': subject,
										'courses': courses}
			)
class CourseDetailView(DetailView):
	model = Course
	template_name = 'courses/course/detail.html'

	# 	use the get_context_data() method to include the enrollment form in the
	# context for rendering the templates. We initialize the hidden course field of the
	# form with the current Course object, so that it can be submitted directly.
	def get_context_data(self, **kwargs):
		context = super(CourseDetailView, self).get_context_data(**kwargs)
		context['enroll_form'] = CourseEnrollForm(
			initial = {'course': self.object})
		return context

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
	
