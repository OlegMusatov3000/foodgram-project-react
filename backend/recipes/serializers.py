from rest_framework import serializers

from recipes.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag
        queryset = Tag.objects.all()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
        queryset = Ingredient.objects.all()
