from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='testuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_step='Recipe Preparation Steps',
            cover='recipes/cover/2024/01/04/imagem_temporaria.jpg',
            )
        recipe.full_clean()
        recipe.save()
        return recipe

    # Change in models.py to True to verify if test will be error
    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.preparation_step_is_html,
            msg='Recipe preparation_step_is_html is not False')

    # Change in models.py to True to verify if test will be error
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False')

    # __str__ in models Recipe
    def test_recipe_string_representation_recipe(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,
            msg='Recipe string representation need to be the same as title\
            "{needed}" but "{str(self.recipe)}"')

    # Test recipe length with module parameterized
    @parameterized.expand(
            [
                ('title', 65),
                ('description', 165),
                ('preparation_time_unit', 65),
                ('servings_unit', 65)
                ]
                )
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
