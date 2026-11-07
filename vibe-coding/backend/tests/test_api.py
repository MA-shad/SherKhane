from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from poetry.models import Poet, Poem, Verse


class SherKhanehAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='Password123!', email='test@sherkhaneh.ir')
        self.poet = Poet.objects.create(name='حافظ شیرازی', slug='hafez', century=8)
        self.poem = Poem.objects.create(poet=self.poet, title='الا یا ایها الساقی', slug='ala-ya-ayyohas-saghi')
        Verse.objects.create(poem=self.poem, order=1, first_couplet='الا یا ایها الساقی ادر کأسا و ناولها', second_couplet='که عشق آسان نمود اول ولی افتاد مشکل‌ها')

    def test_api_root(self):
        response = self.client.get('/api/v1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('endpoints', response.data)

    def test_poets_list(self):
        response = self.client.get('/api/v1/poetry/poets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_poem_search(self):
        response = self.client.get('/api/v1/poetry/poems/?search=الساقی')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_user_registration_and_jwt(self):
        data = {
            'username': 'new_poet',
            'email': 'new_poet@gmail.com',
            'password': 'StrongPassword123!',
            'display_name': 'شاعر نوپا'
        }
        response = self.client.post('/api/v1/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('user', response.data)

    def test_fal_hafez_endpoint(self):
        response = self.client.get('/api/v1/daily/culture/fal_hafez/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tafsir', response.data)
        self.assertIn('verses', response.data)
