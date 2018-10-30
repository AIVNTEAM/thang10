from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInLine(admin.StackedInline):
	model = Choice	#model muon hien thi
	extra = 3	#so luong form bao nhieu

class QuestionAdmin(admin.ModelAdmin):
	#field trong form add - edit
	fieldsets = [
		(None,		{'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date']}),
	]

	# fields = ['question_text','pub_date']
	inlines = [ChoiceInLine]	#hien thi ChoiceInLine o day
	#field trong list question
	list_display = ('question_text', 'pub_date')
	#filter
	list_filter = ['pub_date']
	#search
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)