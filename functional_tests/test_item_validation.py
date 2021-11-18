from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the page and hits the button without printing a single word
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        # After page refresh, she sees an error message
        error_message = self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '.has-error').text)
        # Let's make an assertion regarding this error
        self.assertEqual(error_message, 'Please fill in the form. It can\'t be empty')
        # Edit decides to add one item
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Buy milk')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        # And she sees her new item after page reloads
        self.wait_for_row_in_list_table('1: Buy milk')
        # And somehow she will try again to send an empty form (cp from above). And she receives an error message.
        # Note, these two cases are different: the former - trying to start a new empty list, the latter - trying to
        # add empty field to an existing list. URI differ!!!
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        error_message = self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '.has-error').text)
        self.assertEqual(error_message, 'Please fill in the form. It can\'t be empty')
        # OK, she will make another entry
        self.browser.find_element(By.ID, 'id_new_item').send_keys('Make tee')
        self.browser.find_element(By.ID, 'id_new_item').send_keys(Keys.ENTER)
        # After page reloads, there should be two saved items
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tee')

        self.fail('We have reached the last line of the non-empty-list test')
