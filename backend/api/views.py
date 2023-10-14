from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from favorites.utils import generate_shopping_cart_pdf
from recipes.models import Tag, Ingredient, Recipe
from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializerReadOnly,
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
        return RecipeSerializerReadOnly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class ShoppingCartViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['get'])
#     def download_shopping_cart(self, request):
#         pdf_content = generate_shopping_cart_pdf(request.user)
#         response = Response(pdf_content, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="shopping_cart.pdf"'
#         return response
