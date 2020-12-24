from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название'
        )
    unit = models.CharField(
        max_length=20, verbose_name='Единица измерения', null=True, blank=True
        )
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор"
        )
    title = models.CharField(
        max_length=200, verbose_name='Название'
        )
    image = models.ImageField(
        upload_to='recipes/', blank=True, null=True
        )
    description = models.TextField(
        verbose_name="Описание"
        )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиенты'
        )
    tag = models.CharField(max_length=50, verbose_name='Тег')
    duration = models.PositiveIntegerField(
        verbose_name="Время приготовления в минутах"
        )
    slug = models.SlugField(unique=True, verbose_name='Путь')

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredients'
        )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipes'
        )
    count = models.PositiveIntegerField(verbose_name='Количество')