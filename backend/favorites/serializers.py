from rest_framework import serializers

from .models import Favorite
from recipes.models import Recipe


class FavoriteSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(source='recipe', read_only=True)
    name = serializers.StringRelatedField(source='recipe.name', read_only=True)
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Favorite.objects.filter(
                    recipe__id=self.context['view'].kwargs.get(
                        'recipe_id', None
                    ),
                    user=self.context['request'].user
            ).exists():
                raise serializers.ValidationError(
                    'Упс, рецепт уже добавлен в избранное'
                )
        return data

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
