from rest_framework import serializers

from .models import Favorite
from recipes.models import Recipe
from recipes.serializers import RecipeMiniSerializer


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
        read_only_fields = ('recipe', 'user')

    def validate(self, data):
        recipe_id = self.context['view'].kwargs.get(
                'recipe_id'
            )
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if not Recipe.objects.filter(id=recipe_id).exists():
                raise serializers.ValidationError(
                    'Упс, такого рецепта нет'
                )
            if Favorite.objects.filter(
                recipe__id=recipe_id, user=user
            ).exists():
                raise serializers.ValidationError(
                    'Упс, рецепт уже добавлен в избранное'
                )
        return data

    def to_representation(self, instance):
        return RecipeMiniSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
