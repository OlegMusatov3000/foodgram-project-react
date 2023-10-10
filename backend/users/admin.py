from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name',
        'email', 'is_active', 'role'
    )
    list_display_links = ('id', 'username', 'first_name', 'last_name', 'email')
    list_editable = ('is_active', 'role')
    search_fields = ('username', 'last_name', 'email')
    list_filter = ('email', 'username', 'is_active', 'role')
    empty_value_display = '-пусто-'
    save_on_top = True
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'is_active'
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Тип пользователя'), {'fields': ('role',)})
    )
