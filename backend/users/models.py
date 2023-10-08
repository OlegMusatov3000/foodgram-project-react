from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    '''Класс кастомной модели "User".'''

    class UsersType(models.TextChoices):
        '''Тип пользователей.'''

        GUEST = 'guest', _('Анонимный пользователь')
        AUTHORIZED_USER = 'authorized user', _('Авторизованный пользователь')
        ADMINISTRATOR = 'administrator', _('Aдминистратор')

    role = models.TextField(
        'Пользовательская роль',
        choices=UsersType.choices,
        default=UsersType.AUTHORIZED_USER
    )

    def save(self, *args, **kwargs):
        if (
            not self.pk
            and self.is_superuser
        ):
            self.role = self.UsersType.ADMINISTRATOR
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username}'
