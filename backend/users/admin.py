from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy

from .models import User

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name',
        'email', 'get_count_of_recipes', 'get_count_of_followers',
        'is_active', 'role'
    )
    list_display_links = ('id', 'username', 'first_name', 'last_name', 'email')
    list_editable = ('is_active', 'role')
    search_fields = ('username', 'last_name', 'email')
    list_filter = ('email', 'username', 'is_active', 'role')
    empty_value_display = '-пусто-'
    save_on_top = True
    readonly_fields = (
        'date_joined', 'last_login',
        'get_count_of_recipes', 'get_count_of_followers'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'is_active'
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Тип пользователя'), {'fields': ('role',)}),
        (('Активность пользователя'), {
            'fields': ('get_count_of_recipes', 'get_count_of_followers')
        }),
    )

    def get_count_of_recipes(self, obj):
        return obj.recipes.count()

    get_count_of_recipes.short_description = (
        'Кол-во рецептов пользователя'
    )

    def get_count_of_followers(self, obj):
        return obj.following.count()

    get_count_of_followers.short_description = (
        'Кол-во подписчиков пользователя'
    )
