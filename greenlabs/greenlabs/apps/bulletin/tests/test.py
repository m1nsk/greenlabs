from django.test import Client
from django.test import TestCase
from django.http import Http404
from ..models import Client
from ..services.account_service import user_is_creator, user_is_executor


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

    def test_order_list_success(self):
        c = Client()
        self.assertEqual(c.get('/bulletin/orders/').status_code, 404)

    def test_order_form_success(self):
        c = Client()
        self.te(c.get('/bulletin/orders/form').status_code, 404)

    def test_profile_success(self):
        c = Client()
        self.te(c.get('/bulletin/profile').status_code, 404)

    def test_order_take_fail(self):
        c = Client()
        self.te(c.get('/bulletin/orders/0').status_code, 404)


class AccordanceCreatorTestCase(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        c = Client()
        c.login(username='creator1', password='password123')

    def test_user_is_creator_success(self):
        self.assertEqual(user_is_creator(), True)

    def test_user_is_executor_fail(self):
        self.assertEqual(user_is_executor(), False)

    def test_order_list_success(self):
        c = Client()
        self.assertEqual(c.get('/bulletin/orders/').status_code, 200)

    def test_order_form_success(self):
        c = Client()
        self.te(c.get('/bulletin/orders/form').status_code, 200)

    def test_profile_success(self):
        c = Client()
        self.te(c.get('/bulletin/profile').status_code, 200)

    def test_order_take_fail(self):
        c = Client()
        self.te(c.get('/bulletin/orders/0').status_code, 404)


class AccordanceExecutorTestCase(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        c = Client()
        c.login(username='executor1', password='password123')

    def test_order_list_success(self):
        c = Client()
        self.assertEqual(c.get('/bulletin/orders/').status_code, 200)

    def test_order_form_fail(self):
        c = Client()
        self.te(c.get('/bulletin/orders/form').status_code, 404)

    def test_profile_success(self):
        c = Client()
        self.te(c.get('/bulletin/profile').status_code, 200)

    def test_order_take_success(self):
        c = Client()
        self.te(c.get('/bulletin/orders/0').status_code, 200)