from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_lenght_more_65_raises_error(self):
        self.recipe.title = 'A' * 66
        # will fail if the title has no more than 65 characters
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Aqui a validação ocorre
