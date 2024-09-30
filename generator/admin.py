from django.contrib import admin
from .models import PasswordEntry, User

class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'user')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(PasswordEntry, PasswordEntryAdmin)
admin.site.register(User, UserAdmin)
