from django.shortcuts import render
from django.views import generic
from blog.models import Blogger, Post, Comment
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

# @login_required
class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    # initial = {'post_date': datetime.datetime.now(), 'user' : self.request.user}
    success_url = reverse_lazy('index')

    


def index(request):
    context = {}

    # import os
    # from sendgrid import SendGridAPIClient
    # from sendgrid.helpers.mail import Mail

    # print('Index')

    # message = Mail(
    #     from_email='andriy.oshtuk@gmail.com',
    #     to_emails='andriy.oshtuk@gmail.com',
    #     subject='Sending with Twilio SendGrid is Fun',
    #     html_content='<strong>and easy to do anywhere, even with Python</strong>')
    # try:
    #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    #     print(sg)
    #     print(message)
    #     response = sg.send(message)
    #     print('Send email')
    #     print(response.status_code)
    #     print(response.body)
    #     print(response.headers)
    # except Exception as e:
    #     print(e)
    #     print(e.body)

    return render(request, 'index.html', context=context)


def populate(request):
    context = {}
    fake = Faker()

    for _ in range(5):
        simple_profile = fake.simple_profile()
        nickname = simple_profile.get('username', 'Dummy')
        bio = simple_profile.get('name', 'Dummy')
        blogger = Blogger.objects.create(nickname=nickname, bio=bio)

        for _ in range(5):
            title = fake.text()
            content = fake.text()
            post_date = fake.date_between(start_date='-5y',)
            Post.objects.create(title=title, content=content, post_date=post_date, blogger= blogger)

    return render(request, 'index.html', context=context)