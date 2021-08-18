from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from crm.form import CustomUserCreationForm, CustomUserChangeForm
from crm.models import User, Interaction, Project, Company


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_manager',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_manager',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_manager', 'img')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_manager', 'img')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(Project)
