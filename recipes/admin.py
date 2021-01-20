from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (Ingredient, Recipe, RecipeIngredient,
                     User, Tag, Follow, Favorite, ShoppingList)


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = UserAdmin.list_filter + (
        'email', 'username', "first_name", "last_name",
    )


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)


admin.site.register(Tag, TagAdmin)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit',)
    list_filter = ('title',)


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('author', 'title',)
    list_filter = ('author', 'title', 'tags',)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Recipe, RecipeAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)


admin.site.register(Follow, FollowAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


admin.site.register(Favorite, FavoriteAdmin)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


admin.site.register(ShoppingList, ShoppingListAdmin)
