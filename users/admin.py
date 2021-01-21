from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from recipes.models import User


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = UserAdmin.list_filter + (
        'email', 'username', "first_name", "last_name",
    )


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
