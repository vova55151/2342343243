import django_filters
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import inlineformset_factory
import re
from crm.models import *


# TODO : login(/admin/) редиректит на http://127.0.0.1:8000/accounts/profile/
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


# class CompanyForm(forms.Form):
#     name_comp = forms.CharField()
#     adress = forms.CharField()
#     descr = forms.CharField(widget=forms.Textarea)
#     # date_created = models.DateField()
#     # date_edit = models.DateField()
class EmailModelForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'


class PhoneModelForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        pattern = r'^[0-9\-\+]{9,15}$'
        if re.match(pattern, phone):
            return phone
        else:
            raise forms.ValidationError("Ведите правильный номер телефона")


class NameModelForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        pattern = r'^[\Dа-яА-Яa-zA-Z\D]*$'
        if re.match(pattern, name):
            return name
        else:
            raise forms.ValidationError("Имя должно содержать только буквы")


class CompanyModelForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def clean_name_comp(self):
        name_comp = self.cleaned_data.get('name_comp')
        qs = Company.objects.filter(name_comp__iexact=name_comp)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Введите уникальное название")
        return name_comp


CompanyFormSetEmail = inlineformset_factory(
    Company, Email, form=EmailModelForm,
    fields=['email'], extra=2, can_delete=True
)
CompanyFormSetName = inlineformset_factory(
    Company, Name, form=NameModelForm,
    fields=['name'], extra=2, can_delete=True
)
CompanyFormSetPhone = inlineformset_factory(
    Company, Phone, form=PhoneModelForm,
    fields=['phone'], extra=2, can_delete=True
)


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        pattern = r'^[\W\d\W]*$'
        if re.match(pattern, cost):
            return cost
        else:
            raise forms.ValidationError("Стоимость должна состоять только из цифр")


class InteractionModelForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = '__all__'

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        pattern = r'^[\W\d\W]*$'
        if re.match(pattern, rating):
            return rating
        else:
            raise forms.ValidationError("Рейтинг должен состоять только из цифр")

# class InteractionFilter(django_filters.FilterSet):
#     company = django_filters.CharFilter(lookup_expr='iexact')
#     class Meta:
#         model = Interaction
#         exclude = ['company']
