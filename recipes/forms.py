from django import forms
from .models import Recipe, Ingredient, RecipeIngredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'title', 'tags', 'ingredients', 'duration', 'description', 'image',
            ]
        #labels = {'group': 'Группа', 'text': 'Текст', 'image': 'Картинка'}
        #help_texts = {
            #'group': 'Если знаете тематику, то выберите группу!',
            #'text': 'Постарайтесь выкладывать годный контент!',
            #'image': 'Выберите картинку!'
            #}