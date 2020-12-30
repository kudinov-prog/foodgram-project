from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient, User, Tag, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter =('email', 'username',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


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

admin.site.register(Recipe, RecipeAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)

admin.site.register(Follow, FollowAdmin)