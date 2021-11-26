import django.db.utils
import sqlite3
from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelTest(TestCase):

    def test_creating_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('The first list item', first_saved_item.text)
        self.assertEqual('The second list item', second_saved_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.list, list_)

        self.assertIn(first_saved_item, list_.items.all())

    def test_cannot_save_form_with_missing_text(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_duplicate_items_to_same_list(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Foo')
        with self.assertRaises(sqlite3.IntegrityError and
                               django.db.utils.IntegrityError):
            item_2 = Item.objects.create(list=list_, text='Foo')
            item_2.save()

    @staticmethod
    def test_can_save_those_duplicate_items_to_different_lists():
        list_ = List.objects.create()
        another_list_ = List.objects.create()
        Item.objects.create(list=list_, text='Foo')
        item_2 = Item.objects.create(list=another_list_, text='Foo')
        item_2.full_clean()


class ListModelTest(TestCase):
    def test_can_get_absolute_url(self):
        list_ = List.objects.create()
        url_from_model_method = list_.get_absolute_url()
        hard_coded_url = f'/lists/{list_.id}/'
        self.assertEqual(url_from_model_method, hard_coded_url)
