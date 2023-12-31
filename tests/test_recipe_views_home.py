from .test_recipe_base import RecipeTestBase
from recipes import views
from django.urls import reverse, resolve
from recipes.models import Recipe, Category


class Recipe_views_test_home(RecipeTestBase):
    def test_recipes_home_views_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_home_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('Recipe Title', content)
        self.assertIn('5 Porções', content)

    def test_recipe_home_template_do_not_published(self):
        Recipe.objects.all().delete()
        Category.objects.all().delete()
        """Test recipe is_published=False don't show"""
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))
