from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.views.generic import ListView

PER_PAGE = 9


class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home -- '
        })

        return context


# def index(request):
#     posts = Post.objects.get_published()

#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         }
#     )


def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()
    posts = Post.objects.get_published()\
        .filter(created_by__pk=author_pk)
    user_full_name = user.username

    if user is None:
        raise Http404()

    if (user.first_name):
        user_full_name = f'{user.first_name} {user.last_name}'
    page_title = 'Posts de ' + user_full_name + ' - '

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, *args, **kwargs) -> HttpResponse:
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            # return redirect('blog:index')
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user
        })

        return super().get(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(created_by__pk=self._temp_context['user'].pk)
        return qs

    def get_context_data(self, **kwargs: Any):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username

        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = 'Post de ' + user_full_name + ' - '

        ctx.update({
            'page_title': page_title
        })

        return ctx


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any):
        cxt = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria - '
        cxt.update({
            'page_title': page_title,
        })

        return cxt


# def category(request, slug):
#     posts = Post.objects.get_published()\
#         .filter(category__slug=slug)

#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].category.name} - Categoria - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )

    def get_context_data(self, **kwargs: Any):
        cxt = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - Tag - '
        cxt.update({
            'page_title': page_title,
        })

        return cxt


# def tag(request, slug):
#     posts = Post.objects.get_published()\
#         .filter(tags__slug=slug)

#     paginator = Paginator(posts, 9)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].tags.first().name} - Tag - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


def search(request):
    search_value = request.GET.get('search').strip()
    posts = (
        Post.objects.get_published()
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[0:PER_PAGE]
    )

    if len(posts) == 0:
        raise Http404()

    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )


def page(request, slug):
    page_obj = (
        Page.objects.filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    if page_obj is None:
        raise Http404()

    page_title = f'{page_obj.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_obj,
            'page_title': page_title,
        }
    )


def post(request, slug):
    post_obj = (
        Post.objects.get_published()
        .filter(slug=slug)
        .first()
    )

    if post_obj is None:
        raise Http404()

    page_title = f'{post_obj.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )
