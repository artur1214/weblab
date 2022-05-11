import random

from factory import lazy_attribute
from factory.django import DjangoModelFactory
import factory
from factory.fuzzy import FuzzyInteger


from faker import Faker, Factory

from application.models import Medicine, TypeChoices

fake = Faker('ru_RU')


class MedicineFactory(DjangoModelFactory):
    class Meta:
        model = Medicine

    @lazy_attribute
    def type(self):
        return random.choice(TypeChoices.choices)[0]

    @lazy_attribute
    def name(self):
        res = fake.first_name_male()  # Фейковые имена людей, хз как генерировать случайные препараты.
        res += random.choice(['промин', 'бутин', 'ил', 'ол'])
        return res

    model = fake.company()
    price = FuzzyInteger(50, 5000, step=10)

    @lazy_attribute
    def id(self):
        try:
            last_id = Medicine.objects.latest('id').id
        except Medicine.DoesNotExist:
            last_id = 1
        while Medicine.objects.filter(pk=last_id).exists():
            last_id += 1
        return last_id

