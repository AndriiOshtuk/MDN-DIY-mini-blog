import json
import logging
import os

from django.contrib.auth.models import User

# from blog.models import Post, Blogger, Comment, aos_utils_datetime

from blog.models import Post, Blogger

logger = logging.getLogger(__name__)


""" The default path name to the dummy data json file """
JSON_FILE_PATH = "services/dummy_data.json"


class WilyIgnoreGitRepositoryError(Exception):
    """Error for .wily/ being missing from .gitignore."""

    def __init__(self):
        """Raise runtime error for .gitignore being incorrectly configured."""
        self.message = "Please add '.wily/' to .gitignore before running wily"


class DummyData():
    """Represents a dummy data loaded from a json file."""
    def __init__(self):
        with open(JSON_FILE_PATH, "r") as read_file:
            self.data = json.load(read_file)

    @property
    def users_list(self):
        users = []
        data_items_count = len(self.data['dummy_data'])

        for i in range(data_items_count):
            users.append(self.data['dummy_data'][i]['user'])

        return users

    @property
    def posts_number(self):
        posts_counter = 0

        data_items_count = len(self.data['dummy_data'])

        for i in range(data_items_count):
            posts_counter += len(self.data['dummy_data'][i]['posts'])

        return posts_counter

    def get_user_bio(self, user):
        for name in self.data['dummy_data']:
            if name['user'] == user:
                return name['bio']

        # TODO Add error handling

    def posts_list_for_user(self, user):
        for item in self.data['dummy_data']:
            if item['user'] == user:
                return item['posts']

        # TODO Add error handling

    def convert_json_to_dict(self, record):
        # for name in self.data['dummy_data']:
        #     if name['user'] == user:
        #         return name['bio']

        # TODO Add error handling

        return record['title'], record['date'], record['text']

    def convert_json_to_list(self):
        posts = []
        for user_object in self.data['dummy_data']:
            user_name = user_object['user']
            bio = user_object['bio']

            for record in user_object['posts']:
                title, date, text = self.convert_json_to_dict(record)

                post = {}
                post['user'] = user_name
                post['bio'] = bio
                post['post_title'] = title
                post['post_date'] = date
                post['post_text'] = text

                posts.append(post)

        return posts

    def __str__(self):
        return f'In memory representation of {JSON_FILE_PATH} file'


def populate_db_with_dummy_data():
    """Creates DB records for dummy users as defined by JSON file"""
    logger.info('Populating DB with a default data')

    data = DummyData()
    password = os.getenv('DUMMY_USER_DEFAULT_PASSWORD', None)

    for user in data.users_list:
        dummy_user = User.objects.create_user(username=user, password=password)
        test_blogger = Blogger.objects.create(user=dummy_user, bio=data.get_user_bio(user))
        logger.info(f'Created dummy user {dummy_user}')

        for post in data.posts_list_for_user(user):
            Post.objects.create(
                title=post['title'],
                blogger=test_blogger,
                content=post['text'],
                # post_date = post['date'], # TODO implement post_date
            )
            title = post['title']
            logger.info(f'Created dummy post \"{title}\" for blogger {test_blogger}')


# TODO Move this code out
import unittest
from django.test import TestCase

TEST_USERS = ['elonmusk', 'gvanrossum', 'pycharm', 'skippyhammond']
TEST_POSTS_NUMBER = 14


class TestDummyData(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.data = DummyData()

    def test_list_users(self):
        users = self.data.users_list
        self.assertEqual(users, TEST_USERS)

    def test_posts_number(self):
        posts_number = self.data.posts_number
        self.assertEqual(posts_number, TEST_POSTS_NUMBER)

    def test_get_user_bio(self):
        user_bio = self.data.get_user_bio('pycharm')
        self.assertEqual(user_bio, 'Python IDE for Professional Developers with unique code assistance and analysis, for productive Python, Web and scientific development')

    # def test_convert_json_to_list(self):
    #     posts = self.data.convert_json_to_list()

    #     for p in posts:
    #         print(p)
    #     self.assertEqual(posts_number, TEST_POSTS_NUMBER)

    def test_posts_list_for_user(self):
        posts = self.data.posts_list_for_user('elonmusk')

        for p in posts:
            print(p)
        self.assertEqual(len(posts), 4)


class TestPopulateDb(unittest.TestCase):
    def test_lists_all_data(self):
        populate_db_with_dummy_data()

        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'].title, 'Falcon 9 launc')
        self.assertEqual(str(response.context['post'].blogger), 'elonmusk')
        self.assertEqual(response.context['post'].content, 'Targeting Monday, July 20 for Falcon 9 launch of ANASIS-II from SLC-40')
        # self.assertEqual(response.context['post'].post_date, date.today())
        # self.assertTrue(response.context['comment_list'])
