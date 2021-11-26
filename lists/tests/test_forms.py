from django.test import TestCase
from lists.forms import (
    EMPTY_ITEM_MESSAGE, DUPLICATE_ITEM_MESSAGE, FORM_PLACEHOLDER,
    ItemForm, ExistingListItemForm
)
from lists.models import Item, List


class ItemFormTest(TestCase):

    def test_form_item_input_has_got_placeholder_and_css(self):
        form = ItemForm()
        placeholder_attr = 'placeholder="Enter a to-do item here..."'
        css_attr = 'class="form-control input-lg"'
        self.assertIn(placeholder_attr, form.as_p())
        self.assertIn(css_attr, form.as_p())

    def test_form_validation_for_empty_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'], [EMPTY_ITEM_MESSAGE]
        )

    def test_form_can_perform_save_to_a_correct_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={"text": "do me asap"})
        new_item = form.save_to_this_list(list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me asap')
        self.assertEqual(new_item.list, list_)


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn(FORM_PLACEHOLDER, form.as_p())

    def test_form_validation_for_blank(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_MESSAGE])

    def test_form_validation_for_duplicates(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Some weird text!!!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'Some weird text!!!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_MESSAGE])