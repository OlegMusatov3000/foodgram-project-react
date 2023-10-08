from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name',
        'email', 'is_staff', 'is_active'
    )
    list_display_links = ('username', 'first_name', 'last_name', 'email')
    list_editable = ('is_staff', 'is_active')
    search_fields = ('username', 'last_name', 'email')
    list_filter = ('email', 'username', 'is_staff', 'is_active')
    empty_value_display = '-пусто-'
    save_on_top = True
    readonly_fields = (
        'date_joined', 'last_login'
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
