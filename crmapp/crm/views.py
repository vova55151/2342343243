import django_filters
from ckeditor.widgets import CKEditorWidget
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, FormView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from crm.form import *
from crm.models import Company, Email, Phone, Name, Project, Interaction


# TODO : менеджера добавить в группу и группе выдать права через PRM проверять через .has_perm
class CompanyListView(ListView):
    model = Company
    paginate_by = 10
    template_name = 'company_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['get_ordering'] = self.get_ordering()
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'name_comp')
        return ordering if ordering in {'name_comp', 'date_created'} else 'name_comp'


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'


class CompanyCreateView(CreateView):
    model = Company
    success_url = reverse_lazy('list_comp')
    template_name = 'company_form.html'
    form_class = CompanyModelForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
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
        Обрабатывает запросы POST, создавая экземпляр формы и его встроенные
         наборы форм с переданными переменными POST, а затем их валидация.
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
        Затем редиректит на станицу списка компаний
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
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form,
                                  name_form=name_form))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['name'] = CompanyFormSetName(self.request.POST)
    #         context['email'] = CompanyFormSetEmail(self.request.POST)
    #         context['phone'] = CompanyFormSetPhone(self.request.POST)
    #     else:
    #         context['name'] = CompanyFormSetName().full_clean()
    #         context['email'] = CompanyFormSetEmail().full_clean()
    #         context['phone'] = CompanyFormSetPhone().full_clean()
    #     return context
    #
    # # TODO: ОПТИМИЗИРОВАТЬ ЗАПРОСЫ К БД(django debug tool ne rabotayet)
    # def form_valid(self, form):
    #     context = self.get_context_data(form=form)
    #     formset_name = context['name']
    #     formset_email = context['email']
    #     formset_phone = context['phone']
    #     if formset_name.is_valid() and formset_email.is_valid() and formset_phone.is_valid():
    #         response = super().form_valid(form)
    #         # formset.instance = self.object
    #         # formset.save()
    #         forms = formset_name.save(commit=False)
    #         forms += formset_email.save(commit=False)
    #         forms += formset_phone.save(commit=False)
    #         for form in forms:
    #             form.name = self.object
    #             form.email = self.object
    #             form.phone = self.object
    #             form.save()
    #
    #         return response
    #     else:
    #         return super().form_invalid(form)


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyModelForm
    success_url = reverse_lazy('list_comp')
    template_name = 'company_update.html'

    # def get(self, request, *args, **kwargs):
    #     """
    #
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     phone_form = CompanyFormSetPhone()
    #     email_form = CompanyFormSetEmail()
    #     name_form = CompanyFormSetName()
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               phone_form=phone_form,
    #                               email_form=email_form,
    #                               name_form=name_form))

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

    def form_valid(self, form, phone_form, email_form, name_form):
        """
        Вызывается, если все формы валидны. Создает экземпляр телефона ,контактных лиц и Email
        Затем редиректит на станицу списка компаний
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

        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  phone_form=phone_form,
                                  email_form=email_form,
                                  name_form=name_form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['company_form'] = CompanyModelForm(self.request.POST)
            context['phone_form'] = CompanyFormSetPhone(self.request.POST)
            context['email_form'] = CompanyFormSetEmail(self.request.POST)
            context['name_form'] = CompanyFormSetName(self.request.POST)
        else:
            context['company_form'] = CompanyModelForm()
            context['phone_form'] = CompanyFormSetPhone()
            context['email_form'] = CompanyFormSetEmail()
            context['name_form'] = CompanyFormSetName()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['name'] = CompanyFormSetName(self.request.POST).full_clean()
    #         context['email'] = CompanyFormSetEmail(self.request.POST).full_clean()
    #         context['phone'] = CompanyFormSetPhone(self.request.POST).full_clean()
    #     else:
    #         context['name'] = CompanyFormSetName().full_clean()
    #         context['email'] = CompanyFormSetEmail().full_clean()
    #         context['phone'] = CompanyFormSetPhone().full_clean()
    #     return context
    #
    # def form_valid(self, form):
    #     context = self.get_context_data(form=form)
    #     formset_name = context['name']
    #     formset_email = context['email']
    #     formset_phone = context['phone']
    #     if formset_name.is_valid() and formset_email.is_valid() and formset_phone.is_valid():
    #         response = super().form_valid(form)
    #         formset_name.instance = self.object
    #         formset_name.save()
    #         formset_email.instance = self.object
    #         formset_email.save()
    #         formset_phone.instance = self.object
    #         formset_phone.save()
    #         return response
    #     else:
    #         return super().form_invalid(form)


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy('list_comp')
    template_name = 'company_confirm_delete.html'


class ProjectListView(ListView):
    model = Project
    paginate_by = 10
    template_name = 'project_list.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectModelForm
    success_url = reverse_lazy('list_proj')
    template_name = 'project_form.html'


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectModelForm
    success_url = reverse_lazy('list_proj')
    template_name = 'project_update.html'


class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('proj_list')
    template_name = 'project_confirm_delete.html'


class InteractionFilter(django_filters.FilterSet):
    class Meta:
        model = Interaction
        exclude = []


# class InteractionFilterView(ListView):
#     model = Interaction
#     paginate_by = 10
#     template_name = 'interaction_filter.html'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         filter = InteractionFilter(self.request.GET, queryset)
#         return filter.qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["filter"] = InteractionFilter(self.request.GET, self.get_queryset())
#         return context

class InteractionListView(ListView):
    model = Interaction

    paginate_by = 10
    template_name = 'interaction_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = InteractionFilter(self.request.GET, queryset=Interaction.objects.all())
        context['get_ordering'] = self.get_ordering()
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('sort', 'project')
        return ordering if ordering in {'project', 'rating', 'date_created', 'date_edit'} else 'project'


class InteractionDetailView(DetailView):
    model = Interaction
    template_name = 'interaction_detail.html'


class InteractionCreateView(CreateView):
    model = Interaction
    success_url = reverse_lazy('list_inter')
    form_class = InteractionModelForm
    template_name = 'interaction_form.html'

    def form_valid(self, form):
        manger_form = form.save(commit=False)
        manger_form.manager = self.request.user
        manger_form.save()
        return super(InteractionCreateView, self).form_valid(form)
    # form = InteractionModelForm(request.POST or None)
    #
    # if form.is_valid(self):
    #     your_object = form.save(commit=False)
    #     your_object.user = request.user
    #     your_object.save()
    #     return redirect('your_success_url')


class InteractionUpdateView(UpdateView):
    model = Interaction
    success_url = reverse_lazy('list_inter')
    form_class = InteractionModelForm
    template_name = 'interaction_update.html'
    # TODO : не желательно возвращать набор данных только одного пользователя в get_queryset




class InteractionDeleteView(DeleteView):
    model = Interaction
    success_url = reverse_lazy('list_inter')
    template_name = 'interaction_confirm_delete.html'

