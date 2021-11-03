from django.test import TestCase
from .models import Item, List


class HomePageTest(TestCase):

    def test_uses_right_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_saves_items_only_if_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get(pk=1).text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class ListAndItemModelsTest(TestCase):

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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

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

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

        response = self.client.get(f'/lists/{another_list.id}/')
        self.assertEqual(response.context['list'], another_list)

class NewItemTest(TestCase):

    def test_can_save_POST_request_to_existing_list(self):
        correct_list = List.objects.create()
        another_list = List.objects.create()
        # trying to add an item to list one
        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'Adding a new item to a correct list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Adding a new item to a correct list')
        self.assertEqual(new_item.list, correct_list)
        # trying to add an item to list two
        self.client.post(f'/lists/{another_list.id}/add_item',
                         data={'item_text': 'Why not add an item to another list?'})
        self.assertEqual(Item.objects.count(), 2)
        new_item = Item.objects.get(pk=2)
        self.assertEqual(new_item.text, 'Why not add an item to another list?')
        self.assertEqual(new_item.list, another_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        another_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'Adding a new item to a correct list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
