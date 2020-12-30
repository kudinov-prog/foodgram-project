from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, get_list_or_404

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient, Tag, User, Follow

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


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


class FollowListView(LoginRequiredMixin, ListView):
    paginate_by = 6
    template_name = 'follow.html'
    context_object_name = 'follow'
    def get_queryset(self):
        user = self.request.user
        follows = user.follower.all().values_list('author_id', flat=True)
        chefs = User.objects.filter(id__in=list(follows))
        return chefs


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if not request.user == author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)