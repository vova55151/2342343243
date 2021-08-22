
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import inlineformset_factory
import re
from crm.models import *


class CustomUserCreationForm(UserCreationForm):
    """
    Переопределенная форма создания юзера
    """

    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    """
    Переопределенная форма смены юзера
    """

    class Meta:
        model = User
        fields = ('email',)


class EmailModelForm(forms.ModelForm):
    """
    Модельная форма Email
    """

    class Meta:
        model = Email
        fields = '__all__'


class PhoneModelForm(forms.ModelForm):
    """
    Модельная форма контактов
    """

    class Meta:
        model = Phone
        fields = '__all__'

    def clean_phone(self):
        """
        Вызывается при отправке формы.Проверяет валидность номера телефона
        Возвращает ValidationError,если форма не валидна
        """
        phone = self.cleaned_data.get('phone')
        pattern = r'^[0-9\-\+]{9,15}$'
        if re.match(pattern, phone):
            return phone
        else:
            raise forms.ValidationError("Ведите правильный номер телефона")


class NameModelForm(forms.ModelForm):
    """
    Модельная форма ФИО руководителя (контактного лица)
    """

    class Meta:
        model = Name
        fields = '__all__'

    def clean_name(self):
        """
        Вызывается при отправке формы.Проверяет ,состоит ли имя только из букв
        Возвращает ValidationError,если форма не валидна
        """
        name = self.cleaned_data.get('name')
        pattern = r'^[\Dа-яА-Яa-zA-Z\D]*$'
        if re.match(pattern, name):
            return name
        else:
            raise forms.ValidationError("Имя должно содержать только буквы")


class CompanyModelForm(forms.ModelForm):
    """
    Модельная форма компании
    """

    class Meta:
        model = Company
        fields = '__all__'

    def clean_name_comp(self):
        """
        Вызывается при отправке формы.Проверяет ,есть ли аналогичное название компании в БД
        Возвращает ValidationError,если форма не валидна
        """
        name_comp = self.cleaned_data.get('name_comp')
        qs = Company.objects.filter(name_comp__iexact=name_comp)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Введите уникальное название")
        return name_comp


"""
Инлайн формсет Email
"""
CompanyFormSetEmail = inlineformset_factory(
    Company, Email, form=EmailModelForm,
    fields=['email'], extra=2, can_delete=True
)
"""
Инлайн формсет ФИО руководителя (контактного лица)
"""
CompanyFormSetName = inlineformset_factory(
    Company, Name, form=NameModelForm,
    fields=['name'], extra=2, can_delete=True
)
"""
Инлайн формсет телефона
"""
CompanyFormSetPhone = inlineformset_factory(
    Company, Phone, form=PhoneModelForm,
    fields=['phone'], extra=2, can_delete=True
)


class ProjectModelForm(forms.ModelForm):
    """
    Модельная форма проекта
    """

    class Meta:
        model = Project
        fields = '__all__'

    def clean_cost(self):
        """
        Вызывается при отправке формы.Проверяет,состоит ли стоимость только из цифр
        Возвращает ValidationError,если форма не валидна
        """
        cost = self.cleaned_data.get('cost')
        pattern = r'^[\W\d\W]*$'
        if re.match(pattern, cost):
            return cost
        else:
            raise forms.ValidationError("Стоимость должна состоять только из цифр")


class InteractionModelForm(forms.ModelForm):
    """
    Модельная форма взаимодействия
    """

    class Meta:
        model = Interaction
        fields = '__all__'

    def clean_rating(self):
        """
        Вызывается при отправке формы.Проверяет,состоит ли рейтинг только из цифр от 0 до 5
        Возвращает ValidationError,если форма не валидна
        """
        rating = self.cleaned_data.get('rating')
        pattern = r'^[0-5]$'
        if re.match(pattern, rating):
            return rating
        else:
            raise forms.ValidationError("Укажите рейтинг от 0 до 5")
