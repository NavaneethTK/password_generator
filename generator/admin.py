from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PasswordEntry, User ,AdminUser

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'gender', 'password')
    fields = ('username', 'email', 'phone_number', 'gender', 'password')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

class AdminUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')



class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_name', 'user', 'generated_password')

admin.site.register(PasswordEntry, PasswordEntryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
