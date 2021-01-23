from django.contrib.auth import get_user_model
from django.db import models
from slugify import slugify

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(
        max_length=50, verbose_name='Тег'
    )
    slug = models.SlugField(blank=True)
    checkbox_style = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Название'
    )
    unit = models.CharField(
        max_length=20, verbose_name='Единица измерения', null=True
    )

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=200, verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/', verbose_name='Изображение'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        through_fields=('recipe', 'ingredient')
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги'
    )
    duration = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах'
    )
    slug = models.SlugField(
        unique=True, verbose_name='Путь'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, blank=True,
        null=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save()


class RecipeIngredient(models.Model):
    amount = models.PositiveIntegerField(verbose_name='Количество')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients' #recipes
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_follow'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_favorite'
            )
        ]


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopper',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_list',
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='unique_shoplist'
            )
        ]
