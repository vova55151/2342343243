from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib.auth.models import Group

from crm.form import CustomUserCreationForm, CustomUserChangeForm
from crm.models import User, Interaction, Project, Company


class GroupInstanceInline(admin.TabularInline):
    model = Group


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_manager',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_manager',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_manager', 'img', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_manager', 'img', 'user_permissions',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    #inlines = [GroupInstanceInline]

admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(Project)
