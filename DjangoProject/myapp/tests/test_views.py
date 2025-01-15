from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from myapp.models import Product
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class ProductTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Temporary product', price=1.99, available=True)
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})

        self.regular_user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword')

        self.regular_user_token = str(AccessToken.for_user(self.regular_user))
        self.admin_user_token = str(AccessToken.for_user(self.admin_user))

    def setUp_client(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_all_products_as_regular_user(self):
        self.setUp_client(self.regular_user_token)
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_all_products_as_admin_user(self):
        self.setUp_client(self.admin_user_token)
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Temporary product')
        self.assertEqual(response.data[0]['price'], '1.99')
        self.assertTrue(response.data[0]['available'])

    def test_get_single_product_as_regular_user(self):
        self.setUp_client(self.regular_user_token)
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_get_single_product_as_admin_user(self):
        self.setUp_client(self.admin_user_token)
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Temporary product')
        self.assertEqual(response.data['price'], '1.99')
        self.assertTrue(response.data['available'])

    def test_create_product_as_regular_user(self):
        self.setUp_client(self.regular_user_token)
        data = {"name": "New Product", "price": 5.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_as_admin_user(self):
        self.setUp_client(self.admin_user_token)
        data = {"name": "New Product", "price": 5.99, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')
        self.assertEqual(response.data['price'], '5.99')
        self.assertTrue(response.data['available'])

    def test_update_product_as_regular_user(self):
        self.setUp_client(self.regular_user_token)
        data = {"name": "Updated Product"}
        response = self.client.put(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_as_admin_user(self):
        admin_token = str(AccessToken.for_user(self.admin_user))  # Corrected line
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        data = {
            "name": "Updated Product",
            "price": "15.99",
            "available": True,
        }
        response = self.client.patch(self.product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')
        self.assertEqual(response.data['price'], '15.99')
        self.assertTrue(response.data['available'])

    def test_delete_product_as_regular_user(self):
        self.setUp_client(self.regular_user_token)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product_as_admin_user(self):
        self.setUp_client(self.admin_user_token)
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_with_invalid_data(self):
        self.setUp_client(self.admin_user_token)
        data = {"name": "", "price": -1, "available": True}
        response = self.client.post(self.product_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_invalid_endpoint(self):
        self.setUp_client(self.regular_user_token)
        invalid_url = '/api/invalid-endpoint/'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)