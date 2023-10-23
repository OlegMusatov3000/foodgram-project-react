from django.core.management.base import BaseCommand
import pandas as pd

from foodgram_backend.settings import CSV_INGREDIENTS_PATH, CSV_TAGS_PATH
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Загрузка данных ингредиентов'

    def handle(self, *args, **kwargs):
        data = pd.read_csv(
            CSV_INGREDIENTS_PATH,
            names=['name', 'measurement_unit']
        )
        for _, row in data.iterrows():
            Ingredient.objects.get_or_create(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )

        data = pd.read_csv(CSV_TAGS_PATH, names=['name', 'color', 'slug'])
        for _, row in data.iterrows():
            Tag.objects.get_or_create(
                name=row['name'],
                color=row['color'],
                slug=row['slug']
            )
