from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    color_code = models.CharField(max_length=7, default='#49B64E', unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.SmallIntegerField()
    units = models.CharField(max_length=50)

    def __str__(self):
        return self.name
