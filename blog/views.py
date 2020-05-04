from django.shortcuts import render
from django.views import generic
from blog.models import Blogger, Post

# Create your views here.
class BloggerListView(generic.ListView):
    model = Blogger


class BloggerDetailView(generic.DetailView):
    model = Blogger


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post


def index(request):
    context = {}
    return render(request, 'index.html', context=context)