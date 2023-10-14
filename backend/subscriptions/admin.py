from django.contrib import admin

from .models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    save_on_top = True
