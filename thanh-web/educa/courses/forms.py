from django import forms
from django.forms.models import inlineformset_factory
from .models import User, Course, Module, Student, Teacher
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

#ModuleFormSet cho phep nhieu form cung thuoc 1 module lien ket
ModuleFormSet = inlineformset_factory(
					Course, 
					Module,
					fields=['title', 'description'],
					extra = 2,
					can_delete = True
				)

class StudentSignupForm(UserCreationForm):
	#Student dang nhu la 1 profile vaoi interests la extra-data
	class Meta(UserCreationForm.Meta):
		model = User

	# transaction.atomic, to make sure those 
	# three operations are done in a single database 
	# transaction and avoid data inconsistencies in case of error.
	@transaction.atomic
	def save(self):
		user = super(StudentSignupForm, self).save(commit=False)
		user.is_student = True
		user.save()

		student = Student.objects.create(user=user)
		
		return user

class TeacherSignupForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User

	# transaction.atomic, to make sure those 
	# three operations are done in a single database 
	# transaction and avoid data inconsistencies in case of error.
	@transaction.atomic
	def save(self):
		user = super(TeacherSignupForm, self).save(commit=False)
		user.is_teacher = True
		user.save()
		
		teacher = Teacher.objects.create(user=user)
		return user
