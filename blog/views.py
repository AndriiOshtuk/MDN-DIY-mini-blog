from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from blog.models import Blogger, Post, Comment
from django.urls import reverse
from faker import Faker

# Create your views here.
class BloggerListView(generic.ListView):
    model = Blogger


class BloggerDetailView(generic.DetailView):
    model = Blogger


class PostListView(generic.ListView):
    model = Post
    paginate_by = 20


class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(post__title__contains=context['post'])
        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
import datetime
from django.shortcuts import render, get_object_or_404

# @login_required
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    success_url = reverse_lazy('index')

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
    context = {}
    return render(request, 'index.html', context=context)


def populate(request):
    context = {}
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
