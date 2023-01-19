from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import *


class NewsList(ListView):
    queryset = Post.objects.filter(categoryType='nw')
    ordering = '-dateCreation'
    context_object_name = 'News'
    template_name = 'news/news.html'


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
    model = Post
    context_object_name = 'Post'
    template_name = 'news/post.html'


class Post(DetailView):
    model = Post
    context_object_name = 'Detail'
    template_name = 'news/post_detail.html'
