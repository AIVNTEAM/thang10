from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

#ModuleFormSet cho phep nhieu form cung thuoc 1 module lien ket
ModuleFormSet = inlineformset_factory(
					Course, 
					Module,
					fields=['title', 'description'],
					extra = 2,
					can_delete = True
				)