from django.test import TestCase
from django.contrib.auth.models import User

import unittest.mock as mock
import datetime
from pytz import UTC

from blog.models import Blogger, Post, Comment


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
        today = datetime.date.today()
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


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        PostModelTest.mocked_time = datetime.datetime.now(tz=UTC)

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = PostModelTest.mocked_time

            test_user = User.objects.create_user(username='BigBoss', password='1X<ISRUkw+tuK')
            test_blogger = Blogger.objects.create(user=test_user, bio='It is a dummy test blogger')
            test_post = Post.objects.create(
                title='Post 1 title',
                blogger=test_blogger,
                content='Post 1 body'
            )
            Comment.objects.create(text='Dummy comment', user=test_user, post=test_post)

    def test_text_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Description')

    def test_text_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('text').max_length
        self.assertEquals(max_length, 500)

    def test_post_date_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('post_date').verbose_name
        self.assertEquals(field_label, 'Post date')    

    def test_post_date_is_today(self):
        comment = Comment.objects.get(id=1)
        self.assertEquals(comment.post_date, PostModelTest.mocked_time)

    def test_post_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'Post')

    def test_post_name(self):
        comment = Comment.objects.get(id=1)
        self.assertEquals(str(comment.post), 'Post 1 title')

    def test_user_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'User')

    def test_user_name(self):
        comment = Comment.objects.get(id=1)
        self.assertEquals(str(comment.post.blogger), 'BigBoss')

    def test_object_name_is_comment_text(self):
        comment = Comment.objects.get(id=1)
        self.assertEquals(comment.text, str(comment))
