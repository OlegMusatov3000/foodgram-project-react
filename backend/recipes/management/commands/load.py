import django
from django.core.management.base import BaseCommand
import pandas as pd

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Загрузка данных ингредиентов'

    def handle(self, *args, **kwargs):
        django.setup()

        csv_ingredients_path = 'data/ingredients.csv'
        data = pd.read_csv(csv_ingredients_path, names=['name', 'measurement_unit'])
        for _, row in data.iterrows():
            Ingredient.objects.get_or_create(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )

        csv_tags_path = 'data/tags.csv'
        data = pd.read_csv(csv_tags_path, names=['name', 'color', 'slug'])
        for _, row in data.iterrows():
            Tag.objects.get_or_create(
                name=row['name'],
                color=row['color'],
                slug=row['slug']
            )
