from rest_framework import serializers

from recipes.serializers import RecipeMiniSerializer
from .models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return RecipeMiniSerializer(
            instance=instance.recipe,
            context={'request': self.context.get('request')}
        ).data
