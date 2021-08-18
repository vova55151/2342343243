from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _

from crm.managers import CustomUserManager
from crmapp import settings


# TODO : CompanyUpdateView не передаются данные из реквеста в форму

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_manager = models.BooleanField(default=False, verbose_name='Статус менеджера')
    img = models.ImageField(blank=True, null=True, verbose_name='Фото профиля')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Company(models.Model):
    name_comp = models.CharField(max_length=100, verbose_name='Название')
    descr = RichTextField(blank=True, null=True, verbose_name='Описание', )
    date_created = models.DateField(auto_now_add=True)
    date_edit = models.DateField(auto_now=True)
    adress = models.CharField(max_length=100, verbose_name='Адрес')

    def __str__(self):
        return str(self.name_comp)

    def get_absolute_url(self):
        return reverse('detail_comp', args=[str(self.pk)])


class Email(models.Model):
    email = models.EmailField(verbose_name='Email')
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return str(self.email)


class Phone(models.Model):
    phone = models.CharField(max_length=100, verbose_name='Телефон')
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return str(self.phone)


class Name(models.Model):
    name = models.CharField(max_length=100, verbose_name='Контактное лицо')
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.PROTECT, verbose_name='Компания')
    name = models.CharField(max_length=100, verbose_name='Название')
    descr = RichTextField(max_length=500, blank=True, null=True, verbose_name='Описание')
    date_start = models.DateField(verbose_name='Дата начала работ')
    date_end = models.DateField(verbose_name='Дата окончания работ')
    cost = models.CharField(max_length=100, verbose_name='Стоимость')
    date_created = models.DateField(auto_now_add=True)
    date_edit = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_proj', args=[str(self.pk)])


class Interaction(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.PROTECT, verbose_name='Проект')
    channel = (
        ('З', "Заявка"),
        ('П', "Письмо"),
        ('С', "Сайт"),
        ('И', "Инициатива компании")
    )

    channel_of_reference = models.CharField(choices=channel, max_length=20, verbose_name='Канал обращения')
    descr = RichTextField(max_length=500, blank=True, null=True, verbose_name='Описание')
    rating = models.CharField(max_length=10, blank=True, null=True, verbose_name='Рейтинг')
    manager = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, editable=False,
                                null=True,
                                verbose_name='Менеджер')
    date_created = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_edit = models.DateField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f'Менеджер : {self.manager} Проект :{self.project} Канал связи : {self.channel_of_reference} ' \
               f'Дата создания : {self.date_created}'

    def get_absolute_url(self):
        return reverse('detail_inter', args=[str(self.pk)])
