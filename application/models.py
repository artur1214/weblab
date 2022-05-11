from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    steam_user_id = models.CharField(max_length=100, null=True)
    vk_id = models.CharField(max_length=25, null=True, unique=True)

    @classmethod
    def vk_users(cls):
        return cls.objects.filter(vk_id__isnull=False)

    class Meta:
        app_label = 'application'


class TypeChoices(models.IntegerChoices):
    TABS = 1, _('Таблетки')
    DRINK = 2, _('Сироп')
    DRUG = 3, _('Наркотические вещества')
    PAINKILLER = 4, _('Обезболивающее')


class Medicine(models.Model):
    type = models.IntegerField(choices=TypeChoices.choices,
                               default=TypeChoices.TABS)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'

    class Meta:
        app_label = 'application'



