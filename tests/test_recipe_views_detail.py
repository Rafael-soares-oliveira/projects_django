from django.urls import reverse
from recipes.models import Category
from .test_recipe_base import RecipeTestBase


class Recipe_views_test_detail(RecipeTestBase):
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_loads_recipes(self):
        # Temporary delete all objects, use only those created for tests
        Category.objects.all().delete()
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:category', args=(recipe.category.id,)))  # type: ignore
        content = response.content.decode('utf-8')
        self.assertIn('Recipe Title', content)

    def test_recipe_detail_returns_404_if_ispublished_none(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.id})  # type:ignore
        )
        self.assertEqual(response.status_code, 404)
