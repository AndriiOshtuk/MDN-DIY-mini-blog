from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User

from unittest import skip
from datetime import date
import unittest.mock as mock

from blog.models import Post, Blogger, Comment


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
        self.assertFalse(response.context['is_paginated'])
        self.assertTrue(len(response.context['blogger_list']) == 8)


class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 25

        test_user1 = User.objects.create_user(username='BigBoss1', password='123456789')
        test_blogger1 = Blogger.objects.create(user=test_user1, bio='It is a dunny test blogger 1')
        test_user2 = User.objects.create_user(username='BigBoss2', password='123456789')
        test_blogger2 = Blogger.objects.create(user=test_user2, bio='It is a dunny test blogger 2')

        for post_index in range(number_of_posts):

            blogger = test_blogger1 if post_index % 2 else test_blogger2

            Post.objects.create(
                    title=f'Post {post_index} title',
                    blogger=blogger,
                    content=f'Post {post_index} body'
                )

            # with mock.patch('datetime.date.today') as mock_now:
            #     mock_now.return_value = datetime.now(tz=UTC) - timedelta(days=post_index)

            #     Post.objects.create(
            #         title=f'Post {post_index} title',
            #         blogger=blogger,
            #         content=f'Post {post_index} body'
            #     )

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
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['post_list']) == 20)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (blogs) remaining items number
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['post_list']) == 5)

    # TODO Modify setUpTestData() so posts have different creation dates
    def test_posts_ordered_by_due_date(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['post_list']), 20)

        last_date = 0
        for post in response.context['post_list']:
            if last_date == 0:
                last_date = post.post_date
            else:
                print(str(last_date) + 'vs ' + str(post.post_date))
                self.assertTrue(last_date <= post.post_date)
                last_date = post.post_date


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


class PopulateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user('BigBoss', password='123456789', is_staff=True)
        test_user.save()

    def test_redirect_if_not_stuff_member(self):
        response = self.client.get(reverse('populate'))
        self.assertRedirects(response, '/accounts/login/?next=/blog/populate')

    def test_view_uses_correct_template(self):
        self.client.login(username='BigBoss', password='123456789')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_creates_twentyfive_fake_posts(self):
        posts_count = Post.objects.count()
        self.assertEqual(posts_count, 0)

        self.client.login(username='BigBoss', password='123456789')

        response = self.client.get(reverse('populate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(Post.objects.count(), 25)


class CommentCreateViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='BigBoss1', password='123456789')
        test_blogger1 = Blogger.objects.create(user=test_user1, bio='It is a dunny test blogger 1')

        self.test_post = Post.objects.create(
            title='Post title',
            blogger=test_blogger1,
            content='Post body'
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add-comment', kwargs={'pk': self.test_post.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_logged_in_can_access_create_comment_form(self):
        self.client.login(username='BigBoss1', password='123456789')
        response = self.client.get(reverse('add-comment', kwargs={'pk': self.test_post.pk}))

        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_post_if_logged_in(self):
        # unlikely index to match our post!
        sql_max_integer = 9223372036854775807
        self.client.login(username='BigBoss1', password='123456789')
        response = self.client.get(reverse('add-comment', kwargs={'pk': sql_max_integer}))

        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        self.client.login(username='BigBoss1', password='123456789')
        response = self.client.get(reverse('add-comment', kwargs={'pk': self.test_post.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/comment_form.html')

    def test_redirects_to_blog_detail_page_on_success(self):
        comment_text = 'Test comment'
        self.client.login(username='BigBoss1', password='123456789')
        response = self.client.post(
            reverse('add-comment', kwargs={'pk': self.test_post.pk}),
            {'text': comment_text})

        self.assertRedirects(response, reverse('blog-detail', kwargs={'pk': self.test_post.pk}))

    def test_form_empty_text_field(self):
        self.client.login(username='BigBoss1', password='123456789')

        response = self.client.post(reverse('add-comment', kwargs={'pk': self.test_post.pk}), {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'text', 'This field is required.')


class ErrorViewTest(SimpleTestCase):
    def test_404page_uses_correct_template(self):
        # unlikely index to match our post!
        response = self.client.get('/blog/bloggers/9223372036854775807')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertIn('The page you requested can not be found.', response.content.decode('utf-8'))


    @patch('client.get')
    def test_500_page(self, mock_get):
        """ Should check is 500 page correct """
        mock_get.return_value = HttpResponse(status=500) 
        response = self.client.get('/')
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, '500.html')
        self.assertIn('500 - Server Error', response.content.decode('utf-8'))

    # TODO Added testcase for 500 error
    # @mock.patch('blog.views.index.get', views.ErrorHandler.as_view(error_code=500))
    # def test_500_page(self):
    #     """ Should check is 500 page correct """
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 500)
    #     self.assertTemplateUsed(response, '500.html')
    #     self.assertIn('500 - Server Error', response.content.decode('utf-8'))
