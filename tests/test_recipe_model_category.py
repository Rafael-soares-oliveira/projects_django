from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    # Test category title length
    def test_recipe_category_title_max_length_is_65_chars(self):
        category_title = 'A' * 66
        self.category = self.make_category(name=category_title)
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    # __str__ in models Category
    def test_recipe_string_representation_category(self):
        self.category = self.make_category(name='Testing Representation')
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category), 'Testing Representation',
            msg='Recipe string representation need to be the same as title')
