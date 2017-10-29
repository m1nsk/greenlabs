from django.test import Client
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from ..services.account_service import user_is_creator, user_is_executor, registration_service, profile_data_service, order_list_data_service
from ..models import Client as ClientModel, Order
from django.http import HttpRequest
from ..forms import ClientForm
from importlib import import_module


class AccordanceAnonymousTestCase(TestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        c = Client()
        c.login(username='creator1', password='password123')

    """
    def test_registration_service_success(self):
        form = ClientForm(data={'username': "username111", 'password1': "password123", 'password2': "password123", 'type': ClientModel.EXECUTOR, 'amount': 100})
        request = self.client.post("/bulletin/registration")
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore(None)
        if form.is_valid():
            registration_service(form, request)
        self.assertTrue(ClientModel.objects.get(user=form.save()))
        """

    def test_login_enter_success(self):
        c = Client()
        self.assertEqual(c.get('/bulletin/login/').status_code, 200)

    def test_registration_enter_success(self):
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

    def test_profile_data_service(self):
        request = HttpRequest()
        request.user = User.objects.get(username='creator1')
        context = profile_data_service(request)
        client = ClientModel.objects.get(user=request.user)
        order_list = Order.objects.filter(created_by=client)
        self.assertEqual(len(order_list), len(context['order_list']))
        self.assertEqual(context['type'], ClientModel.CUSTOMER)
        self.assertEqual(context['client'], client)


class AccordanceExecutorTestCase(TestCase):
    fixtures = ['fixtures.json']
    user = User.objects.get(username='executor1')

    def setUp(self):
        pass

    def test_user_is_executor_success(self):
        self.assertEqual(user_is_executor(self.user), True)

    def test_user_is_creator_fail(self):
        self.assertEqual(user_is_creator(self.user), False)

    def test_order_list_data_service(self):
        request = HttpRequest()
        request.user = User.objects.get(username='executor1')
        context = order_list_data_service(request)
        order_list = Order.objects.select_related('created_by').filter(status=Order.OPENED)
        self.assertEqual(len(order_list), len(context['order_list']))
        self.assertEqual(context['type'], ClientModel.EXECUTOR)
