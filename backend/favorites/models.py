from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранное'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite'
        )]
