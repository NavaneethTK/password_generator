from django.contrib import admin
from .models import PasswordEntry, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','phone_number','gender','password')
    fields = ('username', 'email', 'phone_number', 'gender', 'password', 'is_active', 'is_staff')

class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'user','generated_password')

admin.site.register(PasswordEntry, PasswordEntryAdmin)
admin.site.register(User, UserAdmin)
