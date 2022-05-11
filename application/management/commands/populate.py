import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from factory import lazy_attribute
from factory.django import DjangoModelFactory
import factory
from factory.fuzzy import FuzzyInteger

from faker import Faker, Factory

from application.management.factories.medicine import MedicineFactory
from application.models import Medicine

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('--count', required=False, default=1, type=int)

    def handle(self, *args, **options):
        k = 0
        for i in range(options.get('count', 1)):
            MedicineFactory.create()
            print(Medicine.objects.last())
            k +=1
        print('Было создано', k, 'записей')