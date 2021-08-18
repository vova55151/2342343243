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
    path('company/list', CompanyListView.as_view(), name='list_comp'),
    path('company/<int:pk>', CompanyDetailView.as_view(), name='detail_comp'),
    path('company/create', CompanyCreateView.as_view(), name='create_comp'),
    path('company/<int:pk>/update', CompanyUpdateView.as_view(), name='update_comp'),
    path('company/<int:pk>/delete', CompanyDeleteView.as_view(), name='delete_comp'),
    path('project/list', ProjectListView.as_view(), name='list_proj'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name='detail_proj'),
    path('project/create', ProjectCreateView.as_view(), name='create_proj'),
    path('project/<int:pk>/update', ProjectUpdateView.as_view(), name='update_proj'),
    path('project/<int:pk>/delete', ProjectDeleteView.as_view(), name='delete_proj'),
    path('interaction/list', InteractionListView.as_view(), name='list_inter'),
    path('interaction/<int:pk>', InteractionDetailView.as_view(), name='detail_inter'),
    path('interaction/create', InteractionCreateView.as_view(), name='create_inter'),
    path('interaction/<int:pk>/update', InteractionUpdateView.as_view(), name='update_inter'),
    path('interaction/<int:pk>/delete', InteractionDeleteView.as_view(), name='delete_inter'),
    #path('interaction/filter', InteractionDeleteView.as_view(), name='filter_inter'),


]


