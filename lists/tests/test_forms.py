from lists.forms import ItemForm
from django.test import TestCase
from lists.forms import EMPTY_ITEM_MESSAGE

class ItemFormTest(TestCase):

    def test_form_item_input_has_got_placeholder_and_css(self):
        form = ItemForm()
        placeholder_attr = 'placeholder="Enter a to-do item here..."'
        css_attr = 'class="form-control input-lg"'
        self.assertIn(placeholder_attr, form.as_p())
        self.assertIn(css_attr, form.as_p())

    def test_form_validation_for_test_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'], [EMPTY_ITEM_MESSAGE]
        )