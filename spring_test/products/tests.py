from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404

import json

from rest_framework import status
from rest_framework.test import APIClient

from products.models import Product
from products.serializers import ProductSerializer

class ProductApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_products_list(self):
        Product.objects.create(sku='52342523', name='Galaxy s7', qty= 3, price='50.00')
        Product.objects.create(sku='1423231', name='Iphone 4', qty=23 , price='24.99')
        result = self.client.get('/v1/products/')
        product = Product.objects.all().order_by('id')
        serializer = ProductSerializer(product, many=True)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_create_product_successful(self):
        payload = {"sku":"1424452", "name":"Ipad 2", "qty":"2", "price":"49.00" }
        result = self.client.post('/v1/products/', payload, format='json')
        exists = Product.objects.filter(sku=payload['sku']).exists()
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_retrieve_product(self):
        sku = '1423231'
        Product.objects.create(sku=sku, name='Iphone 4', qty=23 , price='24.99')
        result = self.client.get('/v1/products/{}/'.format(sku))
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, sku=sku)
        serializer = ProductSerializer(product)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_update_whole_product(self):
        sku = '112431'
        Product.objects.create(sku=sku, name='Ipad mini', qty=23 , price='59.99')
        payload = {"sku":"125246", "name":"Ipad mini 1", "qty": "20", "price":"67.00"}
        result = self.client.put('/v1/products/{}/'.format(sku), json.dumps(payload), content_type='application/json')
        exists = Product.objects.filter(sku=payload['sku']).exists()
        not_exists = Product.objects.filter(sku=sku).exists()
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertTrue(exists)
        self.assertFalse(not_exists)

    def test_update_qty_product(self):
        sku = '998712452'
        Product.objects.create(sku=sku, name='Ipad pro', qty=1 , price='199.99')
        payload = {"update_qty": 3}
        result = self.client.patch('/v1/products/{}/'.format(sku), json.dumps(payload), content_type='application/json')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data['qty'], payload['update_qty'])
        payload = {"add_qty": 2}
        result = self.client.patch('/v1/products/{}/'.format(sku), json.dumps(payload), content_type='application/json')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data['qty'], 5)

    def test_delete_product(self):
        sku = '7871423'
        Product.objects.create(sku=sku, name='Oppo Reno 4', qty=1 , price='149.99')
        exists = Product.objects.filter(sku=sku).exists()
        result = self.client.delete('/v1/products/{}/'.format(sku))
        not_exists = Product.objects.filter(sku=sku).exists()
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(exists)
        self.assertFalse(not_exists)