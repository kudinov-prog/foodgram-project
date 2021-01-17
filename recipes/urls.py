from django.urls import path
from . import views
from .views import shoplist_download


urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("new/", views.new_recipe, name="new_recipe"),
    path("recipe/<int:recipe_id>/edit", views.recipe_edit, name="recipe_edit"),
    # path('new/', RecipeCreateFormView.as_view(), name='new_recipe'),
    path('recipe/<slug:slug>/', views.RecipeDetailView.as_view(),
         name='recipe'),
    path('profile/<str:username>/', views.ProfileListView.as_view(),
         name='profile'),
    path("follow/", views.FollowListView.as_view(), name="follow_index"),
    path("favorite/", views.FavoriteListView.as_view(), name="favorite"),
    path("shopping/", views.ShoppingListView.as_view(), name="shopping_list"),
    path('shopping/download/', shoplist_download, name='shoplist_download'),
]
