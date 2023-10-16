from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)
from rest_framework.response import Response

from djoser.views import UserViewSet

from .paginations import CustomPagination
from .mixins import FavoriteViewSet, SubscriptionViewSet
from .filters import RecipeFilter
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer
from recipes.models import Tag, Ingredient, Recipe
from recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeReadOnlySerializer,
    RecipeSerializer
)
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer
from shopping_cart.models import ShoppingCart
from shopping_cart.serializers import ShoppingCartSerializer
from shopping_cart.utils import generate_shopping_cart_pdf

User = get_user_model()


class CustomUserViewSet(UserViewSet):

    pagination_class = CustomPagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeSerializer
        return RecipeReadOnlySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                return Response(
                    'Рецепт уже есть в списке покупок',
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = ShoppingCartSerializer(
                data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        ShoppingCart.objects.get(recipe=recipe).delete()
        return Response(
            'Рецепт успешно удалён из списка покупок.',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = User.objects.get(id=self.request.user.id)
        if user.shopping_cart_user.exists():
            return generate_shopping_cart_pdf(request, user)
        return Response(
            'Ошибка. Список покупок пуст', status=status.HTTP_404_NOT_FOUND
        )


class FavoriteViewSet(FavoriteViewSet):

    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe_id'

    def get_recipe(self):
        return get_object_or_404(Recipe, id=self.kwargs.get(self.lookup_field))

    def perform_create(self, serializer):
        serializer.save(recipe=self.get_recipe(), user=self.request.user)


class SubscriptionViewSet(SubscriptionViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'user_id'

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def get_author(self):
        return get_object_or_404(User, id=self.kwargs.get(self.lookup_field))

    def validate_and_get_serializer(self):
        author = self.get_author()
        user = self.request.user
        serializer = SubscriptionSerializer(
            data=self.request.data,
            context={'request': self.request, 'author': author}
        )
        serializer.is_valid(raise_exception=True)
        return serializer, author, user

    def create(self, request, *args, **kwargs):
        serializer, _, _ = self.validate_and_get_serializer()
        self.perform_create(serializer)
        return Response(
            {'Подписка успешно создана': serializer.data},
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        _, author, user = self.validate_and_get_serializer()
        Subscription.objects.get(author=author, user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.get_author(), user=self.request.user)
