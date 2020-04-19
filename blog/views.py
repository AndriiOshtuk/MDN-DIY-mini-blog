from django.shortcuts import render
from django.views import generic
from blog.models import Blogger

# Create your views here.
class BloggerListView(generic.ListView):
    model = Blogger


class BloggerDetailView(generic.DetailView):
    model = Blogger


def index(request):
    pass