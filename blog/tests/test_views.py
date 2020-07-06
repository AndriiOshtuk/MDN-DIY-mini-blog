from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User

from unittest import skip
from datetime import date

from blog.models import Post, Blogger, Comment
from blog.views import PostDetailView


class BloggerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_bloggers = 8

        for index in range(number_of_bloggers):
            test_user = User.objects.create_user(username=f'BigBoss{index}', password='123456789')
            Blogger.objects.create(user=test_user, bio=f'It is a dunny test blogger {index}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/bloggers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_list.html')

    def test_lists_all_authors(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)
        self.assertTrue(len(response.context['blogger_list']) == 8)


class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 25

        test_user1 = User.objects.create_user(username='BigBoss1', password='123456789')
        test_blogger1 = Blogger.objects.create(user=test_user1, bio='It is a dunny test blogger 1')
        test_user2 = User.objects.create_user(username='BigBoss2', password='123456789')
        test_blogger2 = Blogger.objects.create(user=test_user2, bio='It is a dunny test blogger 2')

        for post in range(number_of_posts):

            blogger = test_blogger1 if post % 2 else test_blogger2

            Post.objects.create(
                title=f'Post {post} title',
                blogger=blogger,
                content=f'Post {post} body'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        
    def test_pagination_is_correct(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 20)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (blogs) remaining items number
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 5)


class BloggerDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='BigBoss', password='123456789')
        Blogger.objects.create(user=test_user, bio='It is a dunny test blogger 1')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogger/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogger-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogger-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_detail.html')

    def test_lists_all_data(self):
        response = self.client.get(reverse('blogger-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['blogger']), 'BigBoss')
        self.assertEqual(response.context['blogger'].bio, 'It is a dunny test blogger 1')


class PostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='BigBoss', password='123456789')
        test_blogger = Blogger.objects.create(user=test_user, bio='It is a dunny test blogger 1')

        test_post = Post.objects.create(
                title='Post test title',
                blogger=test_blogger,
                content='Post test body'
            )

        Comment.objects.create(text='Correct comment', user=test_user, post=test_post)

        # Create dummy post and comment 
        test_user1 = User.objects.create_user(username='BigBoss1', password='123456789')
        test_blogger1 = Blogger.objects.create(user=test_user1, bio='It is a dunny test blogger 1')

        test_post1 = Post.objects.create(
                title='Post test title 1',
                blogger=test_blogger1,
                content='Post test body 1'
            )

        Comment.objects.create(text='Dummy comment', user=test_user1, post=test_post1)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blog-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_lists_all_data(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'].title, 'Post test title')
        self.assertEqual(str(response.context['post'].blogger), 'BigBoss')
        self.assertEqual(response.context['post'].content, 'Post test body')
        self.assertEqual(response.context['post'].post_date, date.today())
        self.assertTrue(response.context['comment_list'])
    
    def test_comments_displays_for_correct_post(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['comment_list'])
        self.assertEqual(response.context['comment_list'].values()[0]['text'], 'Correct comment')


class IndexViewTest(SimpleTestCase):
    # TODO Added testcase for '/'' redirect to '/blog/' 
    @skip("Not imlemented testcase yet")
    def test_view_root_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_app_root_url_exists_at_desired_location(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


from django.http import HttpRequest 
class PopulateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user('BigBoss', password='123456789', is_staff=True)
        test_user.save()

    def test_redirect_if_not_stuff_member(self):
        response = self.client.get(reverse('populate'))
        self.assertRedirects(response, '/accounts/login/?next=/blog/populate')

    def test_view_uses_correct_template(self):
        login = self.client.login(username='BigBoss', password='123456789')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_creates_twentyfive_fake_posts(self):
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, 0)

        login = self.client.login(username='BigBoss', password='123456789')

        response = self.client.get(reverse('populate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(Post.objects.count(), 25)
