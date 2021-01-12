from django.urls import path, include
from . import views


urlpatterns = [
    path('favorites/', views.Favorites.as_view()),
    path('favorites/<int:recipe_id>', views.Favorites.as_view()),
]