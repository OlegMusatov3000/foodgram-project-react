# Generated by Django 4.2.6 on 2023-10-08 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredient_options_alter_recipe_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': ''},
        ),
        migrations.AlterModelOptions(
            name='recipetag',
            options={'verbose_name': ''},
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recipetag',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recipetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.tag', verbose_name='Ингредиент'),
        ),
    ]
