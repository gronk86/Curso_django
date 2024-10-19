from .test_recipe_base import RecipeTestBase
from parameterized import parameterized
from django.core.exceptions import ValidationError

class RecipeModelsTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = self.make_recipe(
            category_data={'name': 'test Default Category'},
            author_data={'username': 'newuser'},
            title='Custom Recipe Title',
            description='Custom Recipe Description',
            slug='custom-recipe-slug',
            preparation_time=20,
            preparation_time_unit='Horas',
            servings=10,
            servings_unit='Pessoas',
            preparation_steps='Custom Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='recipe preparation_steps_is_html is not false')

    def test_recipe_is_published_is_true(self):
        recipe = self.make_recipe_no_default()  
        recipe.full_clean()
        recipe.save()
        self.assertTrue(recipe.is_published, 
                        msg='recipe is_published is not true')
        
    def test_recipe_string_representation(self):
        self.recipe.title = 'testando representações'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'testando representações')
