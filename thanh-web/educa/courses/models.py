from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
#su dung cho generic relation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

#dinh nghi lop User voi 2 thuoc tinh mo rong
#model cho phep 1 User co the dam nhan nhieu roles
class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)


class Teacher(models.Model):
	#quan he 1-1 voi User
	user = models.OneToOneField(User, 
		on_delete=models.CASCADE, 
		primary_key=True, related_name='teacher')  #mac dinh thuoc tu User truy suat Teacher theo ten model la: teacher
	#cac thuoc tinh them o day....
	phone = models.CharField(max_length=15)
	def __str__(self):
		return self.user.username

class Subject(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	class Meta:
		ordering = ('title',)
	def __str__(self):
		return self.title

class Course(models.Model):
	owner = models.ForeignKey(Teacher,
		related_name='courses_created', null=True, default='-1')
	subject = models.ForeignKey(Subject,
		related_name='courses')
	# students = models.ManyToManyField(Student, 
	# 	related_name='courses_joined', blank=True)
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	overview = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)
	def __str__(self):
		return self.title

class Module(models.Model):
	course = models.ForeignKey(Course, related_name='modules')
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	order = OrderField(blank=True, for_fields=['course'])
	def __str__(self):
		return '{} . {}' . format(self.order, self.title)
	class Meta:
		ordering = ['order']

class Content(models.Model):
	module = models.ForeignKey(Module, related_name='contents')
	content_type = models.ForeignKey(ContentType,
			limit_choices_to={'model__in':(	'text',
											'video',
											'image',
											'file')}
		)
	object_id = models.PositiveIntegerField()
	item = GenericForeignKey('content_type', 'object_id')
	# order la thuoc tinh tuy chinh
	# o day: order se sap xep phu thuoc vao field la module
	# module = 1: order se bat dau 0 -> 1, ...
	# module = 2: order se bat dau lai tu 0 -> 1, 2, 3,...
	order = OrderField(blank=True, for_fields=['module'])
	class Meta:
		ordering = ['order']
#model co so - va la model truu tuong
class ItemBase(models.Model):
	owner = models.ForeignKey(Teacher,
		related_name='%(class)s_related', null=True, default='-1')
	title = models.CharField(max_length=250)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
	def __str__(self):
		return self.title
	# render_to_string() function for rendering a template and
	# returning the rendered content as a string. Each kind of content is rendered using a
	# template named after the content model. We use self._meta.model_name to build
	# the appropriate template name for la. The render() methods provides a common
	# interface for rendering diverse content.
	def render(self):
		return render_to_string('courses/content/{}.html'.format(
			self._meta.model_name), {'item': self})

#cac model ke thua tu model co so nay
class Text(ItemBase):
	content = models.TextField()
class File(ItemBase):
	file = models.FileField(upload_to='files')
class Image(ItemBase):
	file = models.FileField(upload_to='images')
class Video(ItemBase):
	url = models.URLField()

class Student(models.Model):
	#quan he 1-1 voi User
	user = models.OneToOneField(User, 
		on_delete=models.CASCADE, 
		primary_key=True, related_name='student')
	#cac thuoc tinh them o day....
	phone = models.CharField(max_length=15)
	courses_joined = models.ManyToManyField(Course, 
		through='Booking', related_name='students')
	def __str__(self):
		return self.user.username

class Booking(models.Model):
	course = models.ForeignKey(Course, 
		on_delete=models.CASCADE, related_name='booking_courses')
	student = models.ForeignKey(Student, 
		on_delete=models.CASCADE, related_name='booking_courses')
	user = models.ForeignKey(User, related_name='manages') #user quan ly booking
	message = models.CharField(max_length=250)
	status = models.BooleanField(default=0)
	payment_status = models.BooleanField(default=0)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)