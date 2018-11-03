from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class PublishedManager(models.Manager):
	def get_query(self):
		return super(PublishedManager, self).get_query()\
			.filter(status="published")

class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published')
	)
	objects = models.Manager() # The default manager.
	published = PublishedManager() # Our custom manager.

	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	#name of the reverse relationship, from User to Post, is specified in related_name atribute
	author = models.ForeignKey(User, related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	# the date will be saved automatically when creating an object
	created = models.DateTimeField(auto_now_add=True)
	# the date will be updated automatically when saving an object
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices = STATUS_CHOICES, default='draft')
	def get_absolute_url(self):
		#allows you to build URLs by their name and passing optional parameters
		return reverse('blog:post_detail',
						args=[self.publish.year,
							self.publish.strftime('%m'),
							self.publish.strftime('%d'),
							self.slug])
	# The class Meta inside the model contains metadata
	class Meta:
		#descending order by using the negative prefix
		ordering = ('-publish', ) 
		#The __str__() method is the default human-readable representation of the object.
		def __str__(self):
			return self.title

