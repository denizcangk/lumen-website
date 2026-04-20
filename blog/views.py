from django.shortcuts import render, get_object_or_404
from .models import Blog

def blog_list(request):
    posts = Blog.objects.all().order_by('-created_at')
    return render(request, 'core/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    return render(request, 'core/blog_detail.html', {'post': post})