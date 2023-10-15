from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Aвтор'
    )

    class Meta:
        verbose_name = 'Система подписок'
        verbose_name_plural = 'Система подписок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='subscribe to yourself')]
