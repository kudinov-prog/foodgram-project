from decimal import Decimal

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from .models import Ingredient, RecipeIngredient


def save_recipe(request, form):
    '''Функция сохраняет данные при создании и редактировании рецепта.'''
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for tag in form.cleaned_data['tags']:
                recipe.tags.add(tag.id)

            ingredients = []
            for key, value in form.data.items():
                if 'nameIngredient' in key:
                    title = value
                elif 'valueIngredient' in key:
                    amount = Decimal(value.replace(',', '.'))
                elif 'unitsIngredient' in key:
                    unit = value
                    ingredient = get_object_or_404(
                        Ingredient, title=title, unit=unit)
                    ingredients.append(
                        RecipeIngredient(
                            ingredient=ingredient, recipe=recipe, amount=amount)
                    )
            RecipeIngredient.objects.bulk_create(ingredients)
            return None
    except IntegrityError:
        return 400

def get_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if "nameIngredient" in key:
            _ = key.split("_")
            ingredients[ingredient_name] = int(request.POST[f"valueIngredient_{_[1]}"])
    return ingredients
