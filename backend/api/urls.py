from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

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
]
