from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    '''Класс кастомной модели "User".'''

    class UsersType(models.TextChoices):
        '''Тип пользователей.'''

        GUEST = 'guest', _('Анонимный пользователь')
        AUTHORIZED_USER = 'authorized user', _('Авторизованный пользователь')
        ADMINISTRATOR = 'administrator', _('Aдминистратор')

    email = models.EmailField(
        _('Email address'), unique=True, max_length=254,
        help_text='Адрес электронной почты')
    username = models.CharField(
        _('Username'), max_length=150, unique=True,
        help_text='Уникальный юзернейм (не более 150 символов)',
        validators=[RegexValidator(
            r'^[\w.@+-]+\Z', _('Enter a valid username.'), 'invalid'
        )]
    )
    first_name = models.CharField(
        _('first name'), max_length=150,
        help_text='Имя (не более 150 символов)'
    )
    last_name = models.CharField(
        _('last name'), max_length=150,
        help_text='Фамилия (не более 150 символов)'
    )
    password = models.CharField(
        _('Password'), max_length=150,
        help_text='Пароль (не более 150 символов)'
    )
    role = models.TextField(
        'Пользовательская роль',
        choices=UsersType.choices,
        default=UsersType.AUTHORIZED_USER
    )
    LOGIN_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:
            self.role = self.UsersType.ADMINISTRATOR
        self.is_superuser = self.is_staff = (
            self.role == self.UsersType.ADMINISTRATOR
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
