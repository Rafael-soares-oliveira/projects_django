from django.urls import reverse, resolve
from recipes import views
from tests.test_recipe_base import RecipeTestBase, Recipe


class Recipe_views_test_search(RecipeTestBase):
    def test_recipe_search_uses_correct_view_template(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=1')
        self.assertTemplateUsed(response, 'pages/search-page.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Test>'
        response = self.client.get(url)
        self.assertIn('Search for &quot;&lt;Test&gt;&quot;',
                      response.content.decode('utf-8'))

    def test_recipe_search_return_none_if_is_published_is_false(self):
        Recipe.objects.all().delete()
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:search') + '?q=Test')
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        Recipe.objects.all().delete()
        recipe1 = self.make_recipe(title='This is recipe one', slug='one',
                                   author_data={'username': 'one'})
        recipe2 = self.make_recipe(title='This is recipe two', slug='two',
                                   author_data={'username': 'two'})

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={recipe1.title}')
        response2 = self.client.get(f'{search_url}?q={recipe2.title}')
        response_both = self.client.get(f'{search_url}?q=this is recipe')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])

        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
