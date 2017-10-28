from django.test import Client
from django.test import TestCase
from django.http import Http404
from ..models import Client


class AccordanceTestCase(TestCase):
    fixtures = ['fixtures.json']
    def setUp(self):
        pass

    def test_catalog_fine(self):
        c = Client()
        response = c.get('/api/catalog/', {'categories': '1'})
        old_rusty_sword_of_weak_flag = False
        balalaika_flag = False
        for item in response.context['object_list']:
            if item.name == 'old rusty sword of weak':
                old_rusty_sword_of_weak_flag = True
            else:
                if item.name == 'Balalaika':
                    balalaika_flag = True
        self.assertTrue(old_rusty_sword_of_weak_flag and balalaika_flag)

    def test_catalog_fail(self):
        c = Client()
        response = c.get('/api/catalog/', {'categories': '1'})
        old_rusty_sword_of_weak_flag = False
        balalaika_flag = False
        for item in response.context['object_list']:
            if item.name == 'old rusty sword of weak':
                old_rusty_sword_of_weak_flag = True
            else:
                if item.name == 'Balalaika':
                    balalaika_flag = True
        self.assertFalse(not old_rusty_sword_of_weak_flag or not balalaika_flag)

    def test_catalog_filter_limit(self):
        c = Client()
        response = c.get('/api/catalog/', {'limit': '3'})
        self.assertTrue(len(response.context['object_list']) == 3)

    def test_catalog_filter_offset(self):
        c = Client()
        response = c.get('/api/catalog/', {'offset': '3'})
        self.assertTrue(len(response.context['object_list']) == 3)

    def test_catalog_none_parameters(self):
        c = Client()
        response = c.get('/api/catalog/')
        self.assertTrue(len(response.context['object_list']) == 6)

