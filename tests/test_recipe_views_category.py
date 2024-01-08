from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class Recipe_views_test_category(RecipeTestBase):
    def test_recipes_category_views_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)
