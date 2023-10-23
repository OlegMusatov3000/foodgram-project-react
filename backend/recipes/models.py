from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


User = get_user_model()


class Tag(models.Model):

    name = models.CharField('Название', max_length=200, unique=True)
    color = models.CharField(
        'Цветовой код', max_length=7, default='#49B64E', unique=True,
        help_text='Цвет в HEX'
    )
    slug = models.SlugField(
        'Слаг', max_length=250, unique=True,
        validators=[RegexValidator(
            r'^[-a-zA-Z0-9_]+$', _('Enter a valid slug.'), 'invalid'
        )]
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField('Название', max_length=200, unique=True)
    measurement_unit = models.CharField('ед. измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes',
        verbose_name='Тег'
    )
    author = models.ForeignKey(
        User, related_name='recipes',
        verbose_name='Автор рецепта', on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Рецепт'
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', upload_to=settings.MEDIA_FOR_RECIPES)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления', validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='Ингредиент', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class RecipeTag(models.Model):

    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag, verbose_name='Тег', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'
