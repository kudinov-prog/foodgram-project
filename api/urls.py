from django.urls import path
from . import views


urlpatterns = [
    path("ingredients/", views.Ingredients.as_view()),
    path('favorites/', views.Favorites.as_view()),
    path('favorites/<int:recipe_id>', views.Favorites.as_view()),
    path('subscriptions/', views.Follows.as_view()),
    path('subscriptions/<int:author_id>', views.Follows.as_view()),
    path('purchases/', views.Purchases.as_view()),
    path('purchases/<int:recipe_id>', views.Purchases.as_view()),
]
