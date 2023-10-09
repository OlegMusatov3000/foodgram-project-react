from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView

auth_urls = [
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='token-create'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='token-destroy')
]
urlpatterns = [
    path('', include(auth_urls)),
]
