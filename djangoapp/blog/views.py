from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post


def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request, author_pk):
    posts = Post.objects.get_published()\
        .filter(created_by__pk=author_pk)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    posts = Post.objects.get_published()\
        .filter(category__slug=slug)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def tag(request, slug):
    posts = Post.objects.get_published()\
        .filter(tags__slug=slug)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request, slug):
    return render(
        request,
        'blog/pages/page.html'
    )


def post(request, slug):
    post = (
        Post.objects.get_published()
        .filter(slug=slug)
        .first()
    )

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )
