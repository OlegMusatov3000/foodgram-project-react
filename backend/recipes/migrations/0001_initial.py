# Generated by Django 4.2.6 on 2023-10-08 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('color_code', models.CharField(default='#49B64E', max_length=7, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
    ]
