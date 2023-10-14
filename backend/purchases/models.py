from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Purchase(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchase_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchase_recipe',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_purchase'
        )]
