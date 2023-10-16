from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Favorite

User = get_user_model()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    exclude = ('user',)
    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user',)
        return ()

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
