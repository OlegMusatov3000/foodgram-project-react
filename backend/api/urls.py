from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet, IngredientViewSet, RecipeViewSet, FavoriteViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
# router.register(
#     r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
#     basename='favorite'
# )
# router.register(
#     'download_shopping_cart', ShoppingCartViewSet,
#     basename='recipes/download_shopping_cart'
# )

djoser_urls = [
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='token-create'),
    path(
        'auth/token/logout/', TokenDestroyView.as_view(), name='token-destroy'
    )
]
urlpatterns = [
    path('', include(djoser_urls)),
    path('', include(router.urls)),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='favorite'),
]
