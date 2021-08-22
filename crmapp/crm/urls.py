from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from crmapp import settings
from crm.views import CompanyListView, CompanyDetailView, \
    CompanyUpdateView, CompanyCreateView, CompanyDeleteView, ProjectUpdateView, \
    ProjectDetailView, ProjectCreateView, ProjectListView, ProjectDeleteView, \
    InteractionListView, InteractionDetailView, InteractionCreateView, \
    InteractionUpdateView, InteractionDeleteView

urlpatterns = [
    path('company/list', CompanyListView.as_view(), name='list_comp'),  # отображение списка компаний
    path('company/<int:pk>', CompanyDetailView.as_view(), name='detail_comp'),  # отображение информации о компании
    path('company/create', CompanyCreateView.as_view(), name='create_comp'),  # создание компании
    path('company/<int:pk>/update', CompanyUpdateView.as_view(), name='update_comp'),  # редактирование компании
    path('company/<int:pk>/delete', CompanyDeleteView.as_view(), name='delete_comp'),  # удаление компании
    path('project/list', ProjectListView.as_view(), name='list_proj'),  # отображение списка проектов
    path('project/<int:pk>', ProjectDetailView.as_view(), name='detail_proj'),  # отображение информации о проекте
    path('project/create', ProjectCreateView.as_view(), name='create_proj'),  # создание проекта
    path('project/<int:pk>/update', ProjectUpdateView.as_view(), name='update_proj'),  # обновление проекта
    path('project/<int:pk>/delete', ProjectDeleteView.as_view(), name='delete_proj'),  # удаление проекта
    path('interaction/list', InteractionListView.as_view(), name='list_inter'),  # отображение списка взаимодействий
    path('interaction/<int:pk>', InteractionDetailView.as_view(), name='detail_inter'),  # отображение информации о
    # взаимодействии
    path('interaction/create', InteractionCreateView.as_view(), name='create_inter'),  # создание взаимодействия
    path('interaction/<int:pk>/update', InteractionUpdateView.as_view(), name='update_inter'),  # обновление
    # взаимодействия
    path('interaction/<int:pk>/delete', InteractionDeleteView.as_view(), name='delete_inter'),
    # удаление взаимодействия
]
