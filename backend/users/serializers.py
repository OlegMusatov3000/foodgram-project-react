from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from subscriptions.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD, 'id', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request')
            and self.context.get('request').user.is_authenticated
            and Subscription.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists()
        )


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            'id',
            'password',
        )
