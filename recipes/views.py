from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, get_list_or_404

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient, Tag, User, Follow, ShoppingList

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View


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


def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {'page': page, 'paginator': paginator}
        )


class IndexListView(ListView):
    paginate_by = 6
    template_name = 'index.html'
    context_object_name = 'index'
    def get_queryset(self):
        recipes = Recipe.objects.all()
        return recipes


@login_required
def new_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('index')
        return render(request, 'new_recipe.html', {'form': form})
    form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})


def recipe_view(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    
    return render(
        request, 'recipe.html', {'recipe': recipe}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {'page': page, 'paginator': paginator,
                   'author': author})


class ProfileListView(LoginRequiredMixin, ListView): #допилить!!!
    paginate_by = 6
    template_name = 'profile.html'
    context_object_name = 'profile'
    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs.get('username'))


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
