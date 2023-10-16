from rest_framework import serializers

from .models import Favorite
from recipes.serializers import RecipeMiniSerializer


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('recipe', 'user')
        read_only_fields = ('recipe', 'user')

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

    def to_representation(self, instance):
        return RecipeMiniSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
