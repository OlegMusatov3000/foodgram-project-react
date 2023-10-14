from django.contrib import admin

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    save_on_top = True
