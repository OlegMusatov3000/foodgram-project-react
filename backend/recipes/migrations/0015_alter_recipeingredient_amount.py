# Generated by Django 4.2.6 on 2023-10-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_alter_recipetag_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(blank=True, default=1, verbose_name='Количество'),
            preserve_default=False,
        ),
    ]