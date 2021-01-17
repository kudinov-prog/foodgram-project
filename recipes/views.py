import os
from django.db.models import Sum
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .forms import RecipeForm
from .models import Recipe, User, RecipeIngredient, Ingredient
from .utils import get_ingredients

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        "misc/500.html",
        status=500
        )


class IndexListView(ListView):
    """ Вывод главной страницы с рецептами
    """
    paginate_by = 6
    template_name = 'index.html'
    context_object_name = 'index'

    def get_queryset(self):
        recipes = Recipe.objects.all()
        return recipes


class FollowListView(LoginRequiredMixin, ListView):
    """ Вывод страницы с подписками
    """
    paginate_by = 6
    template_name = 'follow.html'
    context_object_name = 'follow'

    def get_queryset(self):
        user = self.request.user
        follows = user.follower.all().values_list('author_id', flat=True)
        chefs = User.objects.filter(id__in=list(follows))
        return chefs


class FavoriteListView(LoginRequiredMixin, ListView):
    """ Вывод страницы с избранными рецептами
    """
    paginate_by = 6
    template_name = 'favorite.html'
    context_object_name = 'favorite'

    def get_queryset(self):
        user = self.request.user
        favorites = user.adder_user.all().values_list('recipe_id', flat=True)
        fav_recipes = Recipe.objects.filter(id__in=list(favorites))
        return fav_recipes


class ShoppingListView(LoginRequiredMixin, ListView):
    """ Вывод страницы со списком покупок
    """
    template_name = 'shopping_list.html'
    context_object_name = 'shopping_list'

    def get_queryset(self):
        user = self.request.user
        shopper = user.shopper.all().values_list('recipe_id', flat=True)
        recipe_list = Recipe.objects.filter(id__in=list(shopper))
        return recipe_list


class ProfileListView(ListView):
    """ Вывод страницы одного из авторов рецептов
    """
    paginate_by = 6
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        author_recipes = Recipe.objects.filter(author=author)
        return author_recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author'] = author
        return context


class RecipeDetailView(DetailView):
    """ Вывод страницы с детальной информацией о рецепте
    """
    model = Recipe
    template_name = 'recipe.html'


@login_required
def shoplist_download(request):
    """ Скачивает список ингридиентов для рецепта из списка покупок
        в формате txt
    """
    user = request.user
    shopping = user.shopper.all().values_list('recipe_id', flat=True)
    ingredients_amount = RecipeIngredient.objects.values(
        'ingredient_id__title', 'ingredient_id__unit').filter(
        recipe_id__in=list(shopping)).annotate(
        total=Sum('amount')).order_by('ingredient')
    complete_name = f'Ингридиенты_{user}.txt'
    with open(complete_name, 'w') as f:
        for i in list(ingredients_amount):
            f.write(
                f'- {i["ingredient_id__title"]} '
                f'({i["ingredient_id__unit"]}) - {i["total"]} \n'
            )
    f = open(complete_name, 'r')
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={complete_name}'
    os.remove(complete_name)
    return response


@login_required
def recipe_add(request):
    """ Страница с формой добавления нового рецепта
    """
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, "Добавьте ингредиенты")
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            for ing_name, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=ing_name)
                recipe_ing = RecipeIngredient(
                    recipe=recipe, ingredient=ingredient, amount=amount
                )
                recipe_ing.save()
            form.save_m2m()
            return redirect("index")
    else:
        form = RecipeForm()
    return render(request, "new_recipe.html", {"form": form})


"""
class RecipeCreateFormView(LoginRequiredMixin, CreateView):

    form_class = RecipeForm
    template_name = 'new_recipe.html'
    success_url = 'index'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        form_data = form.data
        ingredients = [
            key for key in form_data if key.startswith('nameIngredient_')
        ]
        if not ingredients:
            form.add_error(
                'description',
                'Необходимо указать хотя бы один ингредиент для рецепта'
            )
            return self.form_invalid(form)
        instance.save()
        create_ingredients_amounts(instance, form_data)
        form.save_m2m()

        return redirect(self.success_url)
"""