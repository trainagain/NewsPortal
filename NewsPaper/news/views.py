from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import *
from .filters import *
from .forms import *


def NewsList(request):
    posts = Post.objects.filter(categoryType='nw').order_by('-dateCreation')
    paginatorn = Paginator(posts, 5)
    page_numbern = request.GET.get('pagen')
    pagen_obj = paginatorn.get_page(page_numbern)

    articles = Post.objects.filter(categoryType='ar').order_by('-dateCreation')
    paginatora = Paginator(articles, 5)
    page_numbera = request.GET.get('pagea')
    pagea_obj = paginatora.get_page(page_numbera)

    response_data = {'articles': articles, 'posts': posts, 'pagen_obj': pagen_obj, 'pagea_obj': pagea_obj}

    return render(request, 'news/news.html', response_data)


class Article(ListView):
    queryset = Post.objects.filter(categoryType='ar')
    ordering = '-dateCreation'
    context_object_name = 'Article'
    template_name = 'news/article.html'


class Authorlist(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'news/authors.html'


class Posts(ListView):
    queryset = Post.objects.filter(categoryType='nw')
    ordering = '-dateCreation'
    context_object_name = 'Posts'
    template_name = 'news/post.html'


class PostDitail(DetailView):
    model = Post
    context_object_name = 'Detail'
    template_name = 'news/post_detail.html'


class SeeArhive(ListView):
    model = Post
    context_object_name = 'SeeArhive'
    template_name = 'news/search.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = SeArch(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'nw'
        return super().form_valid(form)


class PostArCreate(LoginRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_post',)
    raise_exception = False
    form_class = PostArForm
    model = Post
    template_name = 'news/article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'ar'
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('NewList')
