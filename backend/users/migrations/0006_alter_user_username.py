# Generated by Django 4.2.6 on 2023-10-09 00:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_email_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Уникальный юзернейм (не более 150 символов)', max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+\\Z', 'Enter a valid username.', 'invalid')], verbose_name='Username'),
        ),
    ]