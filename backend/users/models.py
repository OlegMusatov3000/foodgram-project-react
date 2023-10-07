from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    '''Класс кастомной модели "User".'''

    class UsersType(models.TextChoices):
        '''Тип пользователей.'''

        GUEST = 'guest', _('Анонимный пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Админ')

    role = models.TextField(
        'Пользовательская роль',
        blank=True,
        choices=UsersType.choices,
        default=UsersType.GUEST
    )
