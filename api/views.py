import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from recipes.models import (
    User, Recipe, Follow, Favorite, ShoppingList, Ingredient
)


class Favorites(LoginRequiredMixin, View):
    """ Функция добавления/ удаления рецепта из "Избранного"
    """
    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get('id', None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            _, created = Favorite.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        return JsonResponse({'success': False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(
            Favorite, recipe=recipe_id, user=request.user
        )
        recipe.delete()
        return JsonResponse({'success': True})


class Follows(LoginRequiredMixin, View):
    """ Функция добавления/ удаления подписок
    """
    def post(self, request):
        req_ = json.loads(request.body)
        author_id = req_.get('id', None)
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            if request.user == author:
                return JsonResponse({'success': False})
            _, created = Follow.objects.get_or_create(
                user=request.user, author=author
            )
            if created:
                return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        return JsonResponse({'success': False}, status=400)

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        removed = Follow.objects.filter(
            user=request.user, author=author
            ).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class Purchases(LoginRequiredMixin, View):
    """ Функция добавления/ удаления рецептов в список покупок
    """
    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get('id', None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            _, created = ShoppingList.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if created:
                return JsonResponse({'success': True})
            return JsonResponse({'success': False})
        return JsonResponse({'success': False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        removed = ShoppingList.objects.filter(
            user=request.user, recipe=recipe
            ).delete()
        if removed:
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class Ingredients(LoginRequiredMixin, View):
    """ Функция получения списка ингредиентов
    """
    def get(self, request):
        text = request.GET["query"]
        ingredients = list(
            Ingredient.objects.filter(title__icontains=text).values(
                "title", "unit"
            )
        )
        return JsonResponse(ingredients, safe=False)
