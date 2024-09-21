from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad

# Create your tests here.
class TestAds(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Create some ads for the test user
        Ad.objects.create(title='Ad 1', description='Description 1', user=self.user)
        Ad.objects.create(title='Ad 2', description='Description 2', user=self.user)

    def test_ads(self):
        response = self.client.get('/ads/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ad 1')
        self.assertContains(response, 'Ad 2')