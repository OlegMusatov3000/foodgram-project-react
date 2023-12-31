# Generated by Django 4.2.6 on 2023-10-09 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(help_text='Имя (не более 150 символов)', max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='Фамилия (не более 150 символов)', max_length=150, verbose_name='last name'),
        ),
    ]
