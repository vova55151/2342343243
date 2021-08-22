import django_filters
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from crm.form import *
from crm.models import Company, Project, Interaction


class CompanyListView(ListView):
    """
    Класс для отображения списка компаний
    """
    model = Company
    paginate_by = 10

    template_name = 'company_list.html'

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст с сортировкой
        """
        context = super().get_context_data(**kwargs)

        context['get_ordering'] = self.get_ordering()
        return context

    def get_ordering(self):
        """
        Возвращает сортировку по имени компании или дате создания.По умолчанию сортирует по имени компании
        """
        ordering = self.request.GET.get('sort', 'name_comp')
        return ordering if ordering in {'name_comp', 'date_created'} else 'name_comp'


class CompanyDetailView(DetailView):
    """
    Класс для отображения информации о компании
    """
    model = Company
    template_name = 'company_detail.html'


class CompanyCreateView(UserPassesTestMixin, CreateView):
    """
    Класс для создания компании
    """
    model = Company
    success_url = reverse_lazy('list_comp')
    template_name = 'company_form.html'
    form_class = CompanyModelForm

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает запросы GET
        Возвращает пустую форму и ее встроенные наборы форм.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        phone_form = CompanyFormSetPhone()
        email_form = CompanyFormSetEmail()
        name_form = CompanyFormSetName()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form,
                                  name_form=name_form))

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает запросы POST, создавая экземпляр формы и его встроенные наборы форм с переданными переменными POST
         Возвращает методы валидации формы
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        phone_form = CompanyFormSetPhone(self.request.POST)
        email_form = CompanyFormSetEmail(self.request.POST)
        name_form = CompanyFormSetName(self.request.POST)
        if (form.is_valid() and phone_form.is_valid() and
                email_form.is_valid() and name_form.is_valid()):
            return self.form_valid(form, phone_form, email_form, name_form)
        else:
            return self.form_invalid(form, phone_form, email_form, name_form)

    def form_valid(self, form, phone_form, email_form, name_form):
        """
        Вызывается, если все формы валидны. Создает экземпляр телефона ,контактных лиц и Email
        Возвращает редирект на страницу списка компаний
        """
        self.object = form.save()
        phone_form.instance = self.object
        phone_form.save()
        email_form.instance = self.object
        email_form.save()
        name_form.instance = self.object
        name_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, phone_form, email_form, name_form):
        """
        Вызывается, если форма не валидна.
        Возвращает данные контекста с заполненными данными формы и ошибками.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form,
                                  name_form=name_form))

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated and self.request.user.is_manager:
            return True
        else:
            False


class CompanyUpdateView(UpdateView, UserPassesTestMixin):
    """
    Класс для редактирования компании
    """
    model = Company
    form_class = CompanyModelForm
    success_url = reverse_lazy('list_comp')
    template_name = 'company_update.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated and self.request.user.is_manager:
            return True
        else:
            False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['company_form'] = CompanyModelForm(self.request.POST)
            context['phone_form'] = CompanyFormSetPhone(self.request.POST)
            context['email_form'] = CompanyFormSetEmail(self.request.POST)
            context['name_form'] = CompanyFormSetName(self.request.POST)
        else:
            context['company_form'] = CompanyModelForm()
            context['phone_form'] = CompanyFormSetPhone(instance=self.object)
            context['email_form'] = CompanyFormSetEmail(instance=self.object)
            context['name_form'] = CompanyFormSetName(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        phone_form = context['phone_form']
        email_form = context['email_form']
        name_form = context['name_form']
        if form.is_valid() and phone_form.is_valid() and email_form.is_valid() and name_form.is_valid():
            self.object = form.save()
            phone_form.instance = self.object
            phone_form.save()
            email_form.instance = self.object
            email_form.save()
            name_form.instance = self.object
            name_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    # def get(self, request, *args, **kwargs):
    #     """
    #
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     phone_form = CompanyFormSetPhone(instance=self.object)
    #     email_form = CompanyFormSetEmail(instance=self.object)
    #     name_form = CompanyFormSetName(instance=self.object)
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               phone_form=phone_form,
    #                               email_form=email_form,
    #                               name_form=name_form))
    #
    # def post(self, request, *args, **kwargs):
    #     """
    #     Обрабатывает запросы POST, создавая экземпляр формы и его встроенные
    #      наборы форм с переданными переменными POST, а затем их валидация.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     phone_form = CompanyFormSetPhone(self.request.POST)
    #     email_form = CompanyFormSetEmail(self.request.POST)
    #     name_form = CompanyFormSetName(self.request.POST)
    #     if (form.is_valid() and phone_form.is_valid() and
    #             email_form.is_valid() and name_form.is_valid()):
    #         return self.form_valid(form, phone_form, email_form, name_form)
    #     else:
    #         return self.form_invalid(form, phone_form, email_form, name_form)
    #
    # def form_valid(self, form, phone_form, email_form, name_form):
    #     """
    #     Вызывается, если все формы валидны. Создает экземпляр телефона ,контактных лиц и Email
    #     Затем редиректит на станицу списка компаний
    #     """
    #     self.object = form.save()
    #     phone_form.instance = self.object
    #     phone_form.save()
    #     email_form.instance = self.object
    #     email_form.save()
    #     name_form.instance = self.object
    #     name_form.save()
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def form_invalid(self, form, phone_form, email_form, name_form):
    #     """
    #
    #     """
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               phone_form=phone_form,
    #                               email_form=email_form,
    #                               name_form=name_form))
    #

class CompanyDeleteView(UserPassesTestMixin, DeleteView):
    """
    Класс для удаления компании
    """
    model = Company
    success_url = reverse_lazy('list_comp')
    template_name = 'company_confirm_delete.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False


class ProjectListView(ListView):
    """
    Класс для отображения списка всех проектов
    """
    model = Project
    paginate_by = 10
    template_name = 'project_list.html'


class ProjectDetailView(UserPassesTestMixin, DetailView):
    """
    Класс для отображения информации о проекте
    """
    model = Project
    template_name = 'project_detail.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False


class ProjectCreateView(UserPassesTestMixin, CreateView):
    """
    Класс для создания проекта
    """
    model = Project
    form_class = ProjectModelForm
    success_url = reverse_lazy('list_proj')
    template_name = 'project_form.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False


class ProjectUpdateView(UserPassesTestMixin, UpdateView):
    """
    Класс для редактирования проекта
    """
    model = Project
    form_class = ProjectModelForm
    success_url = reverse_lazy('list_proj')
    template_name = 'project_update.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False


class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    """
    Класс для удаления проекта
    """
    model = Project
    success_url = reverse_lazy('list_proj')
    template_name = 'project_confirm_delete.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False


class InteractionFilter(django_filters.FilterSet):
    """
    Класс для корректной работы фильтра по ключевым словам
    """

    class Meta:
        model = Interaction
        exclude = []


class InteractionListView(UserPassesTestMixin, ListView):
    """
    Класс для отображения списка взаимодействий
    """
    model = Interaction

    paginate_by = 10
    template_name = 'interaction_list.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст с сортировкой и фильтр по ключевым словам
        """
        context = super().get_context_data(**kwargs)
        context["filter"] = InteractionFilter(self.request.GET, queryset=Interaction.objects.all())
        context['get_ordering'] = self.get_ordering()
        return context

    def get_ordering(self):
        """
        Возвращает сортировку по имени проекта,рейтингу,дате создания или дате изменения.
        По умолчанию сортирует по имени проекта
        """
        ordering = self.request.GET.get('sort', 'project')
        return ordering if ordering in {'project', 'rating', 'date_created', 'date_edit'} else 'project'


class InteractionDetailView(UserPassesTestMixin, DetailView):
    """
    Класс для отображения информации о взаимодействии
    """
    model = Interaction
    template_name = 'interaction_detail.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False


class InteractionCreateView(UserPassesTestMixin, CreateView):
    """
    Класс для создания взаимодействия
    """
    model = Interaction
    success_url = reverse_lazy('list_inter')
    form_class = InteractionModelForm
    template_name = 'interaction_form.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        if self.request.user.is_authenticated:
            return self.request.user.is_manager
        else:
            False

    def form_valid(self, form):
        """
        Вызывается, если форма валидна и добавляет к взаимодействию менеджера,которым оно было создано
        """
        manger_form = form.save(commit=False)
        manger_form.manager = self.request.user
        manger_form.save()
        return super(InteractionCreateView, self).form_valid(form)


class InteractionUpdateView(UserPassesTestMixin, UpdateView):
    """
    Класс для редактирования взаимодействия
    """
    model = Interaction
    success_url = reverse_lazy('list_inter')
    form_class = InteractionModelForm
    template_name = 'interaction_update.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        self.object = self.get_object()
        if self.request.user.is_authenticated and self.request.user.is_manager and self.request.user == self.object.manager:
            return True
        else:
            return False


class InteractionDeleteView(UserPassesTestMixin, DeleteView):
    """
    Класс для удаления взаимодействия
    """
    model = Interaction
    success_url = reverse_lazy('list_inter')
    template_name = 'interaction_confirm_delete.html'

    def test_func(self):
        """
        Отклоняет реквест с 403 ошибкой,если метод возвращает False
        """
        self.object = self.get_object()
        if self.request.user.is_authenticated and self.request.user.is_manager and self.request.user == self.object.manager:
            return True
        else:
            return False

