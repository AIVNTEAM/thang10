from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'

# Create your views here.
def post_list(request):
	object_lists = Post.published.all()
	paginator = Paginator(object_lists, 3) # 3 posts each page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer, return page first
		posts = paginator.page(1)
	except EmptyPage:
		# neu vuot qua so luong page
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post, status='published', 
		publish__year=year, 
		publish__month=month,
		publish__day=day)
	return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
	post = get_object_or_404(Post, id=post_id, status="published")
	sent = False

	if request.method == "POST":
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Form fields passed validation
			cd = form.cleaned_data
			#request.build_absolute_uri() to build a
			#complete URL including HTTP schema and hostname
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{}({}) recommends you reading "{}"'.\
				format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.\
				format(post.title, post_url, cd['name'], cd['comment'])
			send_mail(subject, message, 'admin@abc.com', [cd['to']])
			sent = True
			# ... send email

	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', 
		{'post': post, 'form': form, 'sent': sent})
