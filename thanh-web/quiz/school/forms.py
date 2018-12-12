from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from .models import Student, Subject, User, Question, Answer, StudentAnswer

class StudentSignupForm(UserCreationForm):
	#Student dang nhu la 1 profile vaoi interests la extra-data
	interests = forms.ModelMultipleChoiceField(
		queryset=Subject.objects.all(),
		widget=forms.CheckboxSelectMultiple,
		required=True
	)

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
		student.interests.add(*self.cleaned_data.get('interests'))
		#thanh- test cach nay dung ko de thay the dong lenh tren
		# data = self.cleaned_data
		# student.interests.add(data['interests'])
		#end thanh
		return user

class TeacherSignupForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
	def save(self):
		user = super(TeacherSignupForm, self).save(commit=False)
		user.is_teacher = True
		user.save()
		return user

class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(BaseAnswerInlineFormSet, self).clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super(TakeQuizForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
