from django import forms
from courses.models import Course

#form for students to enroll in courses
#form nay chi chua 1 truong ẩn luu thong tin course 
# The course field is
# for the course in which the user gets enrolled
class CourseEnrollForm(forms.Form):
	course = forms.ModelChoiceField(queryset=Course.objects.all(),
		widget=forms.HiddenInput)