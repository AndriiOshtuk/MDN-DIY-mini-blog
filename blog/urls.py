from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index, name='index'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),

    path('blogs/', views.index, name='blogs'),
    path('logout/', views.index, name='logout'),
    path('login/', views.index, name='login'),
    path('post/<int:pk>', views.index, name='post-detail'),
]
