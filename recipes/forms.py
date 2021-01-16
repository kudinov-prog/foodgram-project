from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'title', 'image', 'description', 'tags', 'duration',
            
            ]
        widgets = {'tags': forms.CheckboxSelectMultiple(), }
