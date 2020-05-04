from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Blogger
from datetime import date

class BloggerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_bloggers = 8

        for index in range(number_of_bloggers):
            Blogger.objects.create(nickname=f'Blogger{index}', bio=f'It is a dunny test blogger {index}')

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
        number_of_posts = 8

        test_blogger1 = Blogger.objects.create(nickname='Blogger1', bio='It is a dunny test blogger 1')
        test_blogger2 = Blogger.objects.create(nickname='Blogger2', bio='It is a dunny test blogger 2')

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
        
    def test_pagination_is_ten(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 5)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (blogs) remaining 3 items
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 3)


class BloggerDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Blogger.objects.create(nickname='Blogger 1', bio='It is a dunny test blogger 1')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogger/1')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/blog/blogger/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogger_detail.html')

    def test_lists_all_data(self):
        response = self.client.get('/blog/blogger/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['blogger'].nickname, 'Blogger 1')
        self.assertEqual(response.context['blogger'].bio, 'It is a dunny test blogger 1')


class PostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_blogger = Blogger.objects.create(nickname='Blogger 1', bio='It is a dunny test blogger 1')

        Post.objects.create(
                title='Post test title',
                blogger=test_blogger,
                content='Post test body'
            )
        

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_lists_all_data(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'].title, 'Post test title')
        self.assertEqual(response.context['post'].blogger.nickname, 'Blogger 1')
        self.assertEqual(response.context['post'].content, 'Post test body')
        self.assertEqual(response.context['post'].post_date, date.today())
