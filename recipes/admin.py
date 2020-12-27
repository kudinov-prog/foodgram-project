from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, User, Tag


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter =('email', 'username',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit',)
    list_filter = ('title',)

admin.site.register(Ingredient, IngredientAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)

admin.site.register(Tag, TagAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title',)
    list_filter = ('author', 'title', 'tags',)

admin.site.register(Recipe, RecipeAdmin)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe',)

admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
