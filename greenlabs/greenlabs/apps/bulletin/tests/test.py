from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from ..services.account_service import user_is_creator, user_is_executor,


class AccordanceAnonymousTestCase(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        pass

    def test_login_success(self):
        c = Client()
        self.assertEqual(c.get('/bulletin/login/').status_code, 200)

    def test_registration_success(self):
        c = Client()
        self.assertEqual(c.get('/bulletin/registration/').status_code, 200)


class AccordanceCreatorTestCase(TestCase):
    fixtures = ['fixtures.json']
    user = User.objects.get(username='creator1')

    def setUp(self):
        c = Client()
        c.login(username='creator1', password='password123')

    def test_user_is_creator_success(self):
        self.assertEqual(user_is_creator(self.user), True)

    def test_user_is_executor_fail(self):
        self.assertEqual(user_is_executor(self.user), False)


class AccordanceExecutorTestCase(TestCase):
    fixtures = ['fixtures.json']
    user = User.objects.get(username='executor1')

    def setUp(self):
        c = Client()
        c.login(username='executor1', password='password123')

    def test_user_is_executor_success(self):
        self.assertEqual(user_is_executor(self.user), True)

    def test_user_is_creator_fail(self):
        self.assertEqual(user_is_creator(self.user), False)

