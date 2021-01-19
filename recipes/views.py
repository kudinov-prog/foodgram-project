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
from django.views.generic import ListView, DetailView, CreateView, View


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
        tags_filter = self.request.GET.getlist("filters")
        recipes = Recipe.objects.all()
        if tags_filter:
            recipes = recipes.filter(tags__slug__in=tags_filter).distinct().all()
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
        tags_filter = self.request.GET.getlist("filters")
        user = self.request.user
        favorites = user.adder_user.all().values_list('recipe_id', flat=True)
        fav_recipes = Recipe.objects.filter(id__in=list(favorites))
        if tags_filter:
            fav_recipes = fav_recipes.filter(tags__slug__in=tags_filter).distinct().all()
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
        tags_filter = self.request.GET.getlist("filters")
        author = get_object_or_404(User, username=self.kwargs.get('username'))
        author_recipes = Recipe.objects.filter(author=author)
        if tags_filter:
            author_recipes = author_recipes.filter(tags__slug__in=tags_filter).distinct().all()
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
    user = request.user
    shopping = user.shopper.all().values_list('recipe_id', flat=True)
    ingredients = RecipeIngredient.objects.values(
        'ingredient_id__title', 'ingredient_id__unit').filter(
        recipe_id__in=list(shopping)).annotate(
        total=Sum('amount')).order_by('ingredient')
    file_data = ""
    for item in ingredients:
        line = " ".join(str(value) for value in item.values())
        file_data += line + "\n"
    response = HttpResponse(file_data, content_type="application/text charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="ShoppingList.txt"'
    return response


@login_required
def new_recipe(request):
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


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect("index")
    if request.method == "POST":
        form = RecipeForm(
            request.POST or None, files=request.FILES or None, instance=recipe
        )
        ingredients = get_ingredients(request)
        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for item in ingredients:
                RecipeIngredient.objects.create(
                    ingredient=Ingredient.objects.get(title=f"{item}"),
                    recipe=recipe,
                )
            form.save_m2m()
        return redirect("index")
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    return render(
        request, "recipe_edit.html", {"form": form, "recipe": recipe},
    )


class RecipeEditView(LoginRequiredMixin, View):
    """ Редактирование рецепта
    """
    def get(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.user != recipe.author:
            return redirect(
                'recipe', slug=recipe.slug
            )
        form = RecipeForm(instance=recipe)
        return render(
            request,
            'recipes/recipe_create.html',
            {
                'form': form,
                'recipe': recipe,
            }
        )
    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.user != recipe.author:
            return redirect('index')
        ingridients = recipe.ingridients.all()
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingridients_names = request.POST.getlist('nameIngredient')
        ingridients_values = request.POST.getlist('valueIngredient')
        all_ingridients = collect_ingredients(
            ingridients_names,
            ingridients_values
        )
        if form.is_valid():
            form.save()
            change_ingredients(all_ingridients, ingridients, recipe)
        else:
            return render(
                request,
                'recipes/recipe_create.html',
                {
                    'form': form,
                    'recipe': recipe,
                }
            )
        return redirect('recipe_url', slug=recipe.slug)


@login_required
def recipe_delete(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user == recipe.author:
        recipe.delete()
    return redirect("index")
