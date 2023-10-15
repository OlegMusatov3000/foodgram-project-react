from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from rest_framework.response import Response

from .mixins import FavoriteViewSet, SubscriptionViewSet
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from recipes.models import Tag, Ingredient, Recipe
from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeReadOnlySerializer,
    RecipeSerializer
)
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeSerializer
        return RecipeReadOnlySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(FavoriteViewSet):

    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe_id'

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs.get(self.lookup_field))

    def perform_create(self, serializer):
        serializer.save(recipe=self.get_recipe(), user=self.request.user,)


class SubscriptionViewSet(SubscriptionViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'user_id'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def get_author(self):
        return get_object_or_404(User, id=self.kwargs.get(self.lookup_field))

    def create(self, request, *args, **kwargs):
        author = self.get_author()
        user = self.request.user
        serializer = SubscriptionSerializer(
                data=request.data,
                context={'request': request, 'author': author})
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=author, user=user)
            return Response(
                {'Подписка успешно создана': serializer.data},
                status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        author = self.get_author()
        user = self.request.user
        serializer = SubscriptionSerializer(
                data=request.data,
                context={'request': request, 'author': author})
        if serializer.is_valid(raise_exception=True):
            Subscription.objects.get(author=author, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.get_author(), user=self.request.user)

# class ShoppingCartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['get'])
#     def download_shopping_cart(self, request):
#         pdf_content = generate_shopping_cart_pdf(request.user)
#         response = Response(pdf_content, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="shopping_cart.pdf"'
#         return response
