from django.urls import path

from . import views


urlpatterns = [
    path(
        'ingredients/',
        views.Ingredients.as_view(),
        name='ingredients'
    ),
    path(
        'favorites/',
        views.Favorites.as_view(),
        name='favorites'
    ),
    path(
        'favorites/<int:recipe_id>/',
        views.Favorites.as_view(),
        name='del_favorites'
    ),
    path(
        'subscriptions/',
        views.Follows.as_view(),
        name='subscriptions'
    ),
    path(
        'subscriptions/<int:author_id>/',
        views.Follows.as_view(),
        name='del_subscriptions'
    ),
    path(
        'purchases/',
        views.Purchases.as_view(),
        name='purchases'
    ),
    path(
        'purchases/<int:recipe_id>/',
        views.Purchases.as_view(),
        name='del_purchases'
    ),
]
