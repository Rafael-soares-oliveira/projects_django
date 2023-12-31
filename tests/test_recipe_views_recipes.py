from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class Recipe_views_test_recipes(RecipeTestBase):

    def test_recipes_recipe_views_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_recipe_view_loads_correct_template(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.id}))  # type:ignore
        self.assertTemplateUsed(response, 'pages/recipe-view.html')

    # Test always fail, use for a Work in Progress
    # def test_to_complete(self):
    #     self.fail('Esse teste irá falhar, pois precisa completar')
