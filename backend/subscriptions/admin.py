from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    list_display_links = ('id', 'user', 'author')
    search_fields = ('user', 'author')
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
