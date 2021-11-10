import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10
SLEEP_TIME = 0.5


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f'http://{staging_server}'
        # self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def test_layout_and_styling(self):
        # Edith open the start-page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # She sees that the input-box is centred
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        # If see adds an entry, she sees that her to-do table is also centred
        inputbox.send_keys('Buy some feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some feathers')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (WebDriverException, AssertionError) as e:
                time_elapsed = time.time() - start_time
                if time_elapsed > MAX_WAIT:
                    raise e
                time.sleep(SLEEP_TIME)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith heard of a new app and navigates to its page
        self.browser.get(self.live_server_url)

        # There she sees the page title and h1-header both contain 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('Start', header.text)

        # Then she sees the input form with a placeholder "Enter a to-do item here..."
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual('Enter a to-do item here...', inputbox.get_attribute('placeholder'))

        # She enters "Buy some feathers" and hits the "enter" button
        inputbox.send_keys('Buy some feathers')
        inputbox.send_keys(Keys.ENTER)

        # #fter upd the page should say '1: Buy some feathers'
        self.wait_for_row_in_list_table('1: Buy some feathers')

        # #Edith enters another line: "Make a fly"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Make a fly')
        inputbox.send_keys(Keys.ENTER)

        # After upd the page should show both lines
        self.wait_for_row_in_list_table('1: Buy some feathers')
        self.wait_for_row_in_list_table('2: Make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):

        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy some feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some feathers')

        # Edith checks for her unique url
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Here comes Frances to a completely empty page, so we are quiting and starting the browser again
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy some feathers', page_text)
        self.assertNotIn('Make a fly', page_text)

        # Francis starts his own list
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy some milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy some milk')

        # Francis checks for his unique url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # And his lists has nothing to do with Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy some feathers', page_text)
        self.assertIn('Buy some milk', page_text)
