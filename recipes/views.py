from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, get_list_or_404

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient


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
    paginator = Paginator(recipe_list, 4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {'page': page, 'paginator': paginator}
        )


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
    