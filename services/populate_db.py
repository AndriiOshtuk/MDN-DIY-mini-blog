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
                post_title, post_date, post_text = self.convert_json_to_dict(record)

                post = {}
                post['user'] = user_name
                post['bio'] = bio
                post['post_title'] = post_title
                post['post_date'] = post_date
                post['post_text'] = post_text

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
        Blogger.objects.create(user=dummy_user, bio=data.get_user_bio(user))
        print(f'Create{user}')


# fake = Faker()

#     for _ in range(5):
#         simple_profile = fake.simple_profile()
#         nickname = simple_profile.get('username', 'Dummy')
#         bio = simple_profile.get('name', 'Dummy')
#         user = User.objects.create_user(username=nickname, password='1X<ISRUkw+tuK')
#         blogger = Blogger.objects.create(user=user, bio=bio)

#         for _ in range(5):
#             title = fake.text()
#             content = fake.text()
#             post_date = fake.date_between(start_date='-5y',)
#             Post.objects.create(title=title, content=content, post_date=post_date, blogger=blogger)


import unittest

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
    
    def test_pconvert_json_to_list(self):
        posts = self.data.convert_json_to_list()

        for p in posts:
            print(p)
        self.assertEqual(posts_number, TEST_POSTS_NUMBER)
