from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
# Create your views here.

def post_list(request):
    posts_list = Post.published_manager.all()
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page',1)
    print(request.META)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})

def post_detail(request, year, month, day,post):
    try:
        post = get_object_or_404(Post,
                                 slug=post,
                                 published__year=year,
                                 published__month=month,
                                 published__day=day)
    except Post.DoesNotExist:
        raise Http404("No post found")
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})