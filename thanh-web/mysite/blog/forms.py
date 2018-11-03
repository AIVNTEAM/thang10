from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	comment = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment  # model ma form nay ket noi
		fields = ('name', 'email', 'body') #cac truong su tren form