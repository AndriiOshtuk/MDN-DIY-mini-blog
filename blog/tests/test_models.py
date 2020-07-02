from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Blogger, Post
from datetime import date


class BloggerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='BigBoss', password='1X<ISRUkw+tuK')
        Blogger.objects.create(user=user, bio='It is a dummy test blogger')

    # TODO add test case for username.verbose_name
    # TODO add test case for username.max_length

    def test_bio_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'Bio')

    def test_bio_length(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('bio').max_length
        self.assertEquals(max_length, 300)

    def test_object_name_is_blogger_name(self):
        blogger = Blogger.objects.get(id=1)
        self.assertEquals(blogger.user.username, str(blogger))

    def test_get_absolute_url(self):
        blogger = Blogger.objects.get(id=1)
        self.assertEquals(blogger.get_absolute_url(), '/blog/blogger/1')


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='BigBoss', password='1X<ISRUkw+tuK')
        test_blogger = Blogger.objects.create(user=user, bio='It is a dummy test blogger')
        Post.objects.create(
            title='Post 1 title',
            blogger=test_blogger,
            content='Post 1 body'
        )

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Title')

    def test_title_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 300)

    def test_post_date_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('post_date').verbose_name
        self.assertEquals(field_label, 'Post date')

    def test_post_date_default_value(self):
        post = Post.objects.get(id=1)
        post_date = post.post_date
        today = date.today()
        self.assertEquals(post_date, today)

    def test_content_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'Description')

    def test_content_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('content').max_length
        self.assertEquals(max_length, 5000)

    def test_object_name_is_post_title(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.title, str(post))

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/blog/1')


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='BigBoss', password='1X<ISRUkw+tuK')
        test_blogger = Blogger.objects.create(user=user, bio='It is a dummy test blogger')
        test_post = Post.objects.create(
            title='Post 1 title',
            blogger=test_blogger,
            content='Post 1 body'
        )
        test_date = datetime.datetime.now()
        Comment.objects.create(text='Dummey comment', post_date=test_date, user=test_blogger, post=test_post)
  
