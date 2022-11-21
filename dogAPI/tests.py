from django.test import TestCase

import models
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase




class KeyModelTests(APITestCase, URLPatternsTestCase):

    def test_post_creates_new_key(self):
        response = self.client.post('/api/keys',{'key':'123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(Key.objects.get().key, '123')

    def test_put_increments_value(self):
        response = self.client.put('api/key/123',{}, format='json')
        self.assertEqual(response.data, {'key':'123','value':2})

class CachedImageModelTest(APITestCase, URLPatternsTestCase):

    def test_post_creates_images(self):
        response = self.client.post('api/dogs',{}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED
        self.assertEqual(Cachedimage.objects.count(), 24)

    def test_get_grabs_two_images(self):
        response = self.client.get('api/dogs/1',{}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED
        self.assertEqual(len(response.data), 3)

    

    

        
