import base64
import webcolors
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from favorites.models import Favorite
from shopping_cart.models import ShoppingCart
from users.serializers import CustomUserSerializer


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CookingTimeValidator:
    def __call__(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0 минут.'
            )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    color = Hex2NameColor()

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class RecipeIngredientReadOnlySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredient


class RecipeReadOnlySerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    ingredients = RecipeIngredientReadOnlySerializer(
        many=True, read_only=True, source='recipe_ingredient'
    )
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        return (
            self.context.get('request')
            and self.context.get('request').user.is_authenticated
            and Favorite.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context.get('request')
            and self.context.get('request').user.is_authenticated
            and ShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )


class RecipeMiniSerializer(RecipeReadOnlySerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=[CookingTimeValidator()]
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time'
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags')

        if not ingredients:
            raise serializers.ValidationError(
                'Вы забыли добавить ингридиенты.'
            )

        if not tags:
            raise serializers.ValidationError(
                'Вы забыли добавить теги.'
            )

        ingredients_list = []
        for ingredient_data in ingredients:
            amount = ingredient_data.get('amount')
            if ingredient_data in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты повторяются.'
                )
            if not Ingredient.objects.filter(
                id=ingredient_data.get('id')
            ).exists():
                raise serializers.ValidationError(
                    'Несуществующий ингредиент.'
                )
            if amount is not None and amount <= 1:
                raise serializers.ValidationError(
                    'Нельзя взять ноль ингредиентов.'
                )
            ingredients_list.append(ingredient_data)

        tags_list = []
        for tag_data in tags:
            if tag_data in tags_list:
                raise serializers.ValidationError(
                    'Теги повторяются.'
                )
            tags_list.append(tag_data)

        return data

    def save_recipe(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        common_data = validated_data.copy()

        if instance is not None:
            for field, value in common_data.items():
                setattr(instance, field, value)
            instance.save()

        else:
            instance = Recipe.objects.create(**common_data)

        recipe_ingredients = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            recipe_ingredients.append(RecipeIngredient(
                ingredient_id=ingredient['id'],
                amount=amount,
                recipe=instance
            ))

        with transaction.atomic():
            RecipeIngredient.objects.bulk_create(recipe_ingredients)
            instance.tags.set(tags)
        return instance

    def create(self, validated_data):
        return self.save_recipe(None, validated_data)

    def update(self, instance, validated_data):
        return self.save_recipe(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadOnlySerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
