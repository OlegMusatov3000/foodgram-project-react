from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):

    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited_or_in_shopping_cart'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_favorited_or_in_shopping_cart'
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited_or_in_shopping_cart(self, queryset, name, value):
        related_name = 'favorite_recipe' if name == 'is_favorited' else (
            'shopping_cart_recipe'
        )
        if self.request.user.is_authenticated:
            user_filter = Q(**{f'{related_name}__user': self.request.user})

            if value:
                return queryset.filter(user_filter)
            else:
                return queryset.exclude(user_filter)

        return queryset
