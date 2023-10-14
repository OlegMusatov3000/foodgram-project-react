from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)

from .mixins import FavoriteViewSet
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from recipes.models import Tag, Ingredient, Recipe
from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeReadOnlySerializer,
    RecipeSerializer
)


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
        serializer.is_valid(raise_exception=True)



# class ShoppingCartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['get'])
#     def download_shopping_cart(self, request):
#         pdf_content = generate_shopping_cart_pdf(request.user)
#         response = Response(pdf_content, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="shopping_cart.pdf"'
#         return response
