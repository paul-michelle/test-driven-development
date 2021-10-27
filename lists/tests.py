from django.test import TestCase
from .models import Item
# from django.urls import resolve
# from django.http import HttpRequest
# from .views import home_page

class HomePageTest(TestCase):

    # def test_root_url_resolves_to_home_page_view(self):
    #     found = resolve('/')
    #     self.assertEqual(found.func, home_page)
    #
    #
    # def test_home_page_returns_correct_html(self):
    #     response = self.client.get('/')
    #     html = response.content.decode('utf8').strip()
    #     self.assertTrue(html.startswith('<!'))
    #     self.assertIn('<title>To-Do lists</title>', html)
    #     self.assertTrue(html.endswith('</html>'))
    #
    #     self.assertTemplateUsed(response, 'lists/home.html')

    #_____django client implicitly checks the resolve end function as well as the template used,
    #____ so we can substitute those verbose functions with a short one. Do not forget that your
    #____ templates are nested in lists folder!!!

    def test_uses_right_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get(pk=1).text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_displays_all_list_items(self):
        Item.objects.create(text='item_1')
        Item.objects.create(text='item_2')

        response = self.client.get('/')

        self.assertIn('item_1', response.content.decode())
        self.assertIn('item_2', response.content.decode())

    def test_saves_items_only_if_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

class ItemModelTest(TestCase):

    def test_creating_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('The first list item', first_saved_item.text)
        self.assertEqual('The second list item', second_saved_item.text)

