from django.urls import path
from .views import *

urlpatterns = [
   path('', NewsList.as_view()),
   path('authorlist/', Authorlist.as_view()),
   path('<int:pk>/', Post.as_view()),
   path('article/', Article.as_view()),
   path('article/<int:pk>/', Post.as_view())
]
