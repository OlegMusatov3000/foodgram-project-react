from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from .models import Tag, Ingredient, Recipe, RecipeIngredient, RecipeTag

User = get_user_model()


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.parent_model.__name__ == 'Ingredient':
            self.verbose_name_plural = (
                'В каких рецептах используется:'
            )
        else:
            self.verbose_name_plural = 'Ингридиенты:'


class RecipeTagInline(admin.StackedInline):
    model = RecipeTag
    extra = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.parent_model.__name__ == 'Tag':
            self.verbose_name_plural = (
                'Рецепты для которых прикреплен этот тег:'
            )
        else:
            self.verbose_name_plural = 'Прикрепляемые теги:'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_display_links = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    inlines = (RecipeTagInline,)
    save_on_top = True


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_display_links = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    exclude = ('quantity',)
    inlines = (RecipeIngredientInline,)
    save_on_top = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'get_photo_preview')
    list_display_links = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author')
    inlines = (RecipeIngredientInline, RecipeTagInline)
    exclude = ('author',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = User.objects.get(username=request.user)
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('author', 'get_photo_preview')
        return ()

    def get_photo_preview(self, obj):
        return mark_safe(
            f'<a href="{obj.image.url}"'
            f'target=_blank><img src="{obj.image.url}"'
            'style="max-width: 100px; max-height: 100px;"/></a>'
        )
    get_photo_preview.short_description = 'Как пользователь видит картинку'
