from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet, IngredientViewSet, RecipeViewSet,
    FavoriteViewSet, SubscriptionViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

djoser_urls = [
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='token-create'),
    path(
        'auth/token/logout/', TokenDestroyView.as_view(), name='token-destroy'
    )
]
urlpatterns = [
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='favorite'),
    path(
        'users/subscriptions/',
        SubscriptionViewSet.as_view({'get': 'list'}),
        name='subscriptions-list'),
    path(
        'users/<int:user_id>/subscribe/',
        SubscriptionViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscriptions-post/delete'),
    path('', include(djoser_urls)),
    path('', include(router.urls)),
]
