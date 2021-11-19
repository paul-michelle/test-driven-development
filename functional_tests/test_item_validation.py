from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the page and hits the button without printing a single word
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # After page refresh, she sees an error message. Nope. The page won't refresh due to
        # browser validation: #id_text:invalid. This is browser's pseudo-selector!!!
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))
        # Edit decides to add one item. And the browser error validation message fades away.
        # Now the pseudo-selector is #id_text:valid
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        # And she sees her new item after page reloads
        self.wait_for_row_in_list_table('1: Buy milk')
        # And somehow she will try again to send an empty form (cp from above). And she receives an error message.
        # Note, these two cases are different: the former - trying to start a new empty list, the latter - trying to
        # add empty field to an existing list. URI differ!!!
        self.get_item_input_box().send_keys(Keys.ENTER)
        # And again: browser will detect that #id_text:invalid
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:invalid'))
        # OK, she will make another entry.
        self.get_item_input_box().send_keys('Make tee')
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        # After page reloads, there should be two saved items
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tee')

