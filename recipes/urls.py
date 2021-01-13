from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("new/", views.new_recipe, name="new_recipe"),
    path('recipe/<str:recipe_slug>/', views.recipe_view, name='recipe'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("follow/", views.FollowListView.as_view(), name="follow_index"),
    path("favorite/", views.FavoriteListView.as_view(), name="favorite"),
    path("shopping/", views.ShoppingListView.as_view(), name="shopping_list"),
]
