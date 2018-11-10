from django import template
from django.db.models import Count

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
	return Post.published.count()

@register.inclusion_tag('blog/post/lasted_posts.html')
def show_lasted_posts(count=5):
	lasted_posts = Post.published.order_by('-publish')[:count]
	return {'lasted_posts': lasted_posts}

@register.assignment_tag
def get_most_commented_posts(count=5):
	return Post.published.annotate(total_comments = Count('comments'))\
		.order_by('-total_comments', 'publish')[:count]