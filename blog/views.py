from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from faker import Faker
import datetime

from blog.models import Blogger, Post, Comment


# Create your views here.
class BloggerListView(generic.ListView):
    """
    Display a list of :model:'blog.Blogger'
    
    **Context**
    
    ''blogger_list''
        A list of :model:'blog.Blogger'
    
    **Template:**

    :template:'blog/blogger_list.html'
    
    """
    model = Blogger


class BloggerDetailView(generic.DetailView):
    """
    Display an individual :model:'blog.Blogger'
    
    **Context**
    
    ''blogger''
        An instance of :model:'blog.Blogger'
    
    **Template:**
    
    :template:'blog/blogger_detail.html'
    
    """
    model = Blogger


class PostListView(generic.ListView):
    """
    Display a list of :model:'blog.Post'
    
    **Context**
    
    ''post_list''
        A list of :model:'blog.Post'
    
    **Template:**

    :template:'blog/post_list.html'
    
    """
    model = Post
    paginate_by = 20


class PostDetailView(generic.DetailView):
    """
    Display an individual :model:'blog.Post'
    
    **Context**
    
    ''post''
        An instance of :model:'blog.Post'
    ''comment_list''
        A list of :model:'blog:Comment' related to post
    
    **Template:**
    
    :template:'blog/post_detail.html'
    
    """
    model = Post

    # TODO Redo to use post.comment_set.all in template, then get_context_data() will be obsolete
    def get_context_data(self, **kwargs):
        """ Adds comment_list context variable with a list of commnets for this post"""
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(post__id__exact=context['post'].id)
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        
        """
        #Add logged-in user as author of comment
        form.instance.user = self.request.user
        #Associate comment with blog based on passed id
        form.instance.post=get_object_or_404(Post, pk = self.kwargs['pk'])

        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['post'] = get_object_or_404(Post, pk = self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})


def index(request):
    """
    Display the home page with general site info
    
    **Template:**
    
    :template:'index.html.html'
    
    """
    context = {}
    return render(request, 'index.html', context=context)


# TODO Move business logic to a separate file
@staff_member_required(login_url=reverse_lazy('login'))
def populate(request):
    """
    Utility to populate DB with a fake data fast
    
    """
    context = {} #TODOD remove unused context
    fake = Faker()

    for _ in range(5):
        simple_profile = fake.simple_profile()
        nickname = simple_profile.get('username', 'Dummy')
        bio = simple_profile.get('name', 'Dummy')
        user = User.objects.create_user(username=nickname, password='1X<ISRUkw+tuK')
        blogger = Blogger.objects.create(user=user, bio=bio)

        for _ in range(5):
            title = fake.text()
            content = fake.text()
            post_date = fake.date_between(start_date='-5y',)
            Post.objects.create(title=title, content=content, post_date=post_date, blogger= blogger)

    return render(request, 'index.html', context=context)
