# Generated by Django 4.2.6 on 2023-10-14 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipes'), name='unique_favorite'),
        ),
    ]
