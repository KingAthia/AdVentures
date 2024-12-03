from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
#Test the API views
class ApiTests(TestCase):
    def test_api_login(self):
        response = self.client.post('/api/auth/login/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.json())
        self.assertTrue('id' in response.json()['user'])
        self.assertTrue('username' in response.json()['user'])
        self.assertTrue('email' in response.json()['user'])

    def test_api_register(self):

        response = self.client.post('/api/auth/register/', {'username': 'newuser', 'email': '   [email protected]  ', 'password': 'newpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.json())
        self.assertTrue('id' in response.json()['user'])
        self.assertTrue('username' in response.json()['user'])
        self.assertTrue('email' in response.json()['user'])
        self.assertEqual(response.json()['user']['username'], 'newuser')
        self.assertEqual(response.json()['user']['email'], '   [email protected]  ')
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(User.objects.filter(email='   [email protected]  ').exists())
        self.assertTrue(User.objects.filter(username='newuser', email='   [email protected]  ').exists())
        self.assertTrue(User.objects.get(username='newuser').check_password('newpass'))
        self.assertTrue(User.objects.get(email='   [email protected]  ').check_password('newpass'))
        self.assertTrue(User.objects.get(username='newuser', email='   [email protected]  ').check_password('newpass'))
        self.assertTrue(User.objects.get(username='newuser').is_authenticated)
        self.assertTrue(User.objects.get(email='   [email protected]  ').is_authenticated)
        self.assertTrue(User.objects.get(username='newuser', email='   [email protected]  ').is_authenticated)
        self.assertTrue(User.objects.get(username='newuser').is_active)
        self.assertTrue(User.objects.get(email='   [email protected]  ').is_active)
        self.assertTrue(User.objects.get(username='newuser', email='   [email protected]  ').is_active)
        self.assertTrue(User.objects.get(username='newuser').is_staff)
        self.assertTrue(User.objects.get(email='   [email protected]  ').is_staff)
        self.assertTrue(User.objects.get(username='newuser', email='   [email protected]  ').is_staff)
        self.assertTrue(User.objects.get(username='newuser').is_superuser)

    def test_api_get_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('categories' in response.json())
        self.assertTrue(isinstance(response.json()['categories'], list))
        self.assertTrue(all(isinstance(category, dict) for category in response.json()['categories']))
        self.assertTrue(all('id' in category for category in response.json()['categories']))
        self.assertTrue(all('name' in category for category in response.json()['categories']))
        self.assertTrue(all('price' in category for category in response.json()['categories']))
        self.assertTrue(all(isinstance(category['id'], int) for category in response.json()['categories']))
        self.assertTrue(all(isinstance(category['name'], str) for category in response.json()['categories']))
        self.assertTrue(all(isinstance(category['price'], str) for category in response.json()['categories']))

    def test_api_create_ad(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/api/ads/create/', {'title': 'Test Ad', 'description': 'This is a test ad', 'image': 'test.jpg', 'adCategory': [1, 2]})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('ad' in response.json())
        self.assertTrue('id' in response.json()['ad'])
        self.assertTrue('title' in response.json()['ad'])
        self.assertTrue('description' in response.json()['ad'])
        self.assertTrue('image' in response.json()['ad'])
        self.assertTrue('adCategory' in response.json()['ad'])
        self.assertEqual(response.json()['ad']['title'], 'Test Ad')

    def test_api_calculate_ad_price(self):
        response = self.client.post('/api/ads/calculate-price/', {'adCategory': [1, 2], 'slots': {'1': 2, '2': 3}})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('total_price' in response.json())
        self.assertTrue('subtotals' in response.json())
        self.assertTrue(isinstance(response.json()['total_price'], str))
        self.assertTrue(isinstance(response.json()['subtotals'], dict))
        self.assertTrue(all(isinstance(subtotal, str) for subtotal in response.json()['subtotals'].values()))

    def test_api_process_payment(self):
        response = self.client.post('/api/ads/payment/', {'slots_data': {'1': 2, '2': 3}, 'ad_categories': [1, 2], 'total_price': '100.00'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.json())
        self.assertTrue(response.json()['success'])

    def test_api_get_user_ads(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/api/ads/user/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('ads' in response.json())
        self.assertTrue(isinstance(response.json()['ads'], list))
        self.assertTrue(all(isinstance(ad, dict) for ad in response.json()['ads']))
        self.assertTrue(all('id' in ad for ad in response.json()['ads']))
        self.assertTrue(all('title' in ad for ad in response.json()['ads']))
        self.assertTrue(all('description' in ad for ad in response.json()['ads']))
        self.assertTrue(all('image' in ad for ad in response.json()['ads']))
        self.assertTrue(all('adCategory' in ad for ad in response.json()['ads']))
        self.assertTrue(all(isinstance(ad['id'], int) for ad in response.json()['ads']))
        self.assertTrue(all(isinstance(ad['title'], str) for ad in response.json()['ads']))
        self.assertTrue(all(isinstance(ad['description'], str) for ad in response.json()['ads']))
        self.assertTrue(all(isinstance(ad['image'], str) for ad in response.json()['ads']))
        self.assertTrue(all(isinstance(ad['adCategory'], list) for ad in response.json()['ads']))
        self.assertTrue(all(all(isinstance(category, int) for category in ad['adCategory']) for ad in response.json()['ads']))

    def test_api_get_dashboard_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/api/user/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('dashboard_data' in response.json())
        self.assertTrue(isinstance(response.json()['dashboard_data'], dict))
        self.assertTrue('total_ads' in response.json()['dashboard_data'])
        self.assertTrue('total_categories' in response.json()['dashboard_data'])
        self.assertTrue('total_views' in response.json()['dashboard_data'])
        self.assertTrue(isinstance(response.json()['dashboard_data']['total_ads'], int))
        self.assertTrue(isinstance(response.json()['dashboard_data']['total_categories'], int))
        self.assertTrue(isinstance(response.json()['dashboard_data']['total_views'], int))
        self.assertEqual(response.json()['dashboard_data']['total_ads'], 5)

#Test the Ad views
class AdTests(TestCase):
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_create_ad(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/ads/create/', {'title': 'Test Ad', 'description': 'This is a test ad', 'image': 'test.jpg', 'adCategory': [1, 2]})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/ads/payment/')

    def test_ad_payment(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post('/ads/payment/', {'slots_1': 2, 'slots_2': 3})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/payment.html')

    def test_payment_verification(self):
        response = self.client.post('/ads/payment-verification/', {'payment_id': '123456', 'status': 'success'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/payment-verification.html')

    def test_dashboard(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/user/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/dashboard.html')

