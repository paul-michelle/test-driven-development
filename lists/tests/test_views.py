from pprint import pprint

from django.test import TestCase
from lists.models import Item, List
from lists.forms import ItemForm
from lists.forms import EMPTY_ITEM_MESSAGE
from django.utils.html import escape


class HomePageTest(TestCase):

    def test_uses_right_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_saves_items_only_if_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_homepage_uses_newly_introduced_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get(pk=1).text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_if_validation_errors_than_user_is_sent_back_to_homepage(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_reflected_on_homepage(self):
        response = self.client.post('/lists/new', data={'text': ''})
        error_message = escape(EMPTY_ITEM_MESSAGE)
        self.assertContains(response, error_message)

    def test_when_invalid_input__form_is_still_passed_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_items_are_not_saved_to_db(self):
        self.client.post('/lists/new', data={'text': ''})
        result_of_searching_invalid_item = Item.objects.filter(text='')
        self.assertFalse(result_of_searching_invalid_item)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f'/lists/{list_.id}/', data={'text': ''})

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

        response = self.client.get(f'/lists/{another_list.id}/')
        self.assertEqual(response.context['list'], another_list)

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='item_1', list=correct_list)
        Item.objects.create(text='item_2', list=correct_list)

        another_list = List.objects.create()
        Item.objects.create(text='item_1_another_list', list=another_list)
        Item.objects.create(text='item_2_another_list', list=another_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'item_1')
        self.assertContains(response, 'item_2')
        self.assertNotContains(response, 'item_1_another_list')
        self.assertNotContains(response, 'item_2_another_list')

    def test_can_save_POST_request_to_existing_list(self):
        correct_list = List.objects.create()
        another_list = List.objects.create()
        # trying to add an item to list one
        self.client.post(f'/lists/{correct_list.id}/',
                         data={'text': 'Adding a new item to a correct existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Adding a new item to a correct existing list')
        self.assertEqual(new_item.list, correct_list)
        # trying to add an item to list two
        # self.client.post(f'/lists/{another_list.id}/add_item',
        #                  data={'text': 'Why not add an item to another list?'})
        # self.assertEqual(Item.objects.count(), 2)
        # new_item = Item.objects.get(pk=2)
        # self.assertEqual(new_item.text, 'Why not add an item to another list?')
        # self.assertEqual(new_item.list, another_list)

    def test_redirects_after_POST_to_list_view(self):
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'text': 'Adding a new item to a correct existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_invalid_input_is_not_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_when_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_when_invalid_input_formed_is_passed_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_when_invalid_input_error_is_shown_on_page(self):
        response = self.post_invalid_input()
        error_message = escape(EMPTY_ITEM_MESSAGE)
        self.assertContains(response, error_message)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        pprint(response.context)
        self.assertIsInstance(response.context["form"], ItemForm)
        self.assertContains(response, 'name="text"')
