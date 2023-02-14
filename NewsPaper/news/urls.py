from django.urls import path
from . import views
from .views import *

urlpatterns = [
   path('', views.NewsList, name='NewList'),
   path('edit/', PostUpdate.as_view(), name='update'),
   path('delete/', PostDelete.as_view(), name='delete'),
   path('search/', SeeArhive.as_view()),
   path('search/<int:pk>/', PostDitail.as_view()),
   path('news/', Posts.as_view(), name='post_list'),
   path('news/<int:pk>/', PostDitail.as_view(), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('article/', Article.as_view(), name='article_list'),
   path('article/<int:pk>/', PostDitail.as_view(), name='article_detail'),
   path('article/create/', PostArCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', PostUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),

]
