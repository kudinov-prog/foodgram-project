from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_recipe, name="new_recipe"),
    path('recipe/<str:recipe_slug>/', views.recipe_view, name='recipe'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("follow/", views.FollowListView.as_view(), name="follow_index"),
    path("favorite/", views.FavoriteListView.as_view(), name="favorite"),
    path(
        "<str:username>/follow/",
        views.profile_follow,
        name="profile_follow"
    ), 
    path(
        "<str:username>/unfollow/",
        views.profile_unfollow,
        name="profile_unfollow"
    ),
]
