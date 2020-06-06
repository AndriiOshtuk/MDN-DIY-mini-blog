from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index, name='index'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('blogs/', views.PostListView.as_view(), name='blogs'),
    # path('blog/<int:pk>', views.PostDetailView.as_view(), name='blog-detail'),
    path('<int:pk>', views.PostDetailView.as_view(), name='blog-detail'),

    path('comment/create/', views.CommentCreate.as_view(), name='add-comment'),

    
    # path('logout/', views.index, name='logout'),
    # path('login/', views.index, name='login'),
    
]
