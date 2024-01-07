from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category
from .test_recipe_base import RecipeTestBase, Recipe


class Recipe_views_test(RecipeTestBase):

    # Test view function
    def test_recipe_home_views_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_views_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_recipe_views_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    # Test view status code
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    # Test view template
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    # Test response if no recipe
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    # Test error 404
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    # Test home view with content
    def test_recipe_home_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('Recipe Title', content)
        self.assertIn('5 Porções', content)

    # Test category view with content
    def test_recipe_detail_loads_recipes(self):
        # Temporary delete all objects, use only those created for tests
        Category.objects.all().delete()
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:category', args=(recipe.category.id,)))  # type: ignore
        content = response.content.decode('utf-8')
        self.assertIn('Recipe Title', content)

    # Test recipe is_published=False don't show
    def test_recipe_home_template_do_not_published(self):
        Recipe.objects.all().delete()
        Category.objects.all().delete()
        """Test recipe is_published=False don't show"""
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_detail_returns_404_if_ispublished_none(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'id': recipe.id})  # type:ignore
        )
        self.assertEqual(response.status_code, 404)

    def tearDown(self) -> None:
        return super().tearDown()

    # Test always fail, use for a Work in Progress
    # def test_to_complete(self):
    #     self.fail('Esse teste irá falhar, pois precisa completar')
