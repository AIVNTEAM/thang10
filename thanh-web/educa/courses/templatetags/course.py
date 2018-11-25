from django import template

register = template.Library()

#This is the model_name template filter.
#We can apply it in templates as
# object|model_name to get the model's name for an object.
@register.filter
def model_name(obj):
	try:
		return obj._meta.model_name
	except AttributeError:
		return None