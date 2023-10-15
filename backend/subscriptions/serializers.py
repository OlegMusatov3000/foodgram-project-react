from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Subscription
from recipes.models import Recipe
from recipes.serializers import ForSubscriptionsSerializer

User = get_user_model()


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = ForSubscriptionsSerializer(
        source='author.recipes', many=True, read_only=True
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Subscription.objects.filter(
                user=obj.user,
                author=obj.author
            ).exists()
        return False

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def validate(self, data):
        author = self.context.get('author')
        user = self.context.get('request').user
        if self.context['request'].method == 'POST':
            if Subscription.objects.filter(
                author__id=author.id, user=user
            ).exists():
                raise serializers.ValidationError(
                    'Произошла ошибка. Вы уже подписаны'
                )
            if author == user:
                raise serializers.ValidationError(
                    'Произошла ошибка. Нельзя подписаться на самого себя'
                    )
        elif self.context['request'].method == 'DELETE':
            if not Subscription.objects.filter(
                author__id=author.id, user=user
            ).exists():
                raise serializers.ValidationError(
                        'Произошла ошибка. Вы не были подписаны'
                    )
        return data
