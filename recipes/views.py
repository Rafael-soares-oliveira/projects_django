from django.shortcuts import render
from utils.recipes.fake_register import make_recipe
from .models import Recipe
# Create your views here.


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'pages/home.html',
                  context={'name': 'Rafael Oliveira', 'recipes': recipes, })


def category(request, category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')
    return render(request, 'pages/category.html',
                  context={
                      'recipes': recipes,
                      'title': f'{recipes.first().category.name} - Category | '
                  })


def recipes(request, id):
    return render(request, 'pages/recipe-view.html',
                  context={'name': 'Rafael Oliveira',
                           'recipe': make_recipe(),
                           'is_detail_page': True,
                           })
