from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from rest_framework.response import Response

from application.management.factories.medicine import MedicineFactory
from application.models import Medicine, TypeChoices
from django.test import Client

class MedicineTestCase(TestCase):
    databases = ['default']

    def setUp(self):
        User.objects.create_user('artur1214', '', 'wasd123')
        #MedicineFactory.create()
        s = Medicine.objects.create(
            type=TypeChoices.DRUG,
            name='Фентанил',
            model='ООО Эмаксифарм',
            price=1000
        )
        Medicine.objects.create(type=TypeChoices.PAINKILLER, name='Некст',
            model='ООО Фортелар', price=160)

        Medicine.objects.create(type=TypeChoices.TABS, name='Нурофен',
            model='ООО НУрафен', price=70)
        token_url = reverse('token_obtain_pair')
        jwt_fetch_data = {'username': 'artur1214', 'password': 'wasd123'}
        response = self.client.post(token_url, jwt_fetch_data, format='json')
        token = response.data['access']
        self.client.defaults.update({'HTTP_AUTHORIZATION': f'Bearer {token}'})
        #self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.data = {'type': 1, 'name': 'Тестовое лекарство', 'model': 'ООО ТестКонтора',
        'price': 5000}

    def test_get_medicine(self):
        resp: Response = self.client.get('/api/medicine/')
        self.assertEqual(resp.status_code, 200)
        resp = resp.json()
        self.assertIsNotNone(resp)
        self.assertEqual(len(resp), Medicine.objects.count())

    def test_create_medicine(self):

        resp: Response = self.client.post('/api/medicine/', data=self.data)
        self.assertEqual(resp.status_code, 201)
        created_obj = Medicine.objects.get(**self.data)
        self.assertIsInstance(created_obj, Medicine)


    def test_update_medicine(self):
        data = {'name': 'ещё более тестовое лекарство', 'price': 300}
        self.test_create_medicine()
        resp: Response = self.client.patch(f'/api/medicine/{Medicine.objects.get(**self.data).pk}/', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        #print(resp.data)
        med_obj = Medicine.objects.filter(**data)
        self.assertIsInstance(med_obj, (Medicine, QuerySet))
        self.assertEqual(med_obj[0].name, data['name'])
