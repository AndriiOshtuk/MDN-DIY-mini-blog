import json
import logging

# from django.contrib.auth.models import User

# from blog.models import Post, Blogger, Comment, aos_utils_datetime

logger = logging.getLogger(__name__)


""" The default path name to the dummy data json file """
JSON_FILE_PATH = "services/dummy_data.json"


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

    def get_user_bio(user):
        
    

    def __str__(self):
        return f'In memory representation of {JSON_FILE_PATH} file'


# def populate_db():

#     logger.info('Populating DB with a default data')

#     with open(JSON_FILE_PATH, "r") as read_file:
#         data = json.load(read_file)

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
