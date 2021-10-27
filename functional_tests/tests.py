from django.test import LiveServerTestCase
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        # self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith heard of a new app and navigates to its page
        self.browser.get(self.live_server_url)

        #There she sees the page title and h1-header both contain 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('Start', header.text)

        #Then she sees the input form with a placeholder "Enter a to-do item here..."
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual('Enter a to-do item here...', inputbox.get_attribute('placeholder'))

        # She enters "Buy some feathers" and hits the "enter" button
        inputbox.send_keys('Buy some feathers')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # #fter upd the page should say '1: Buy some feathers'
        self.check_for_row_in_list_table('1: Buy some feathers')

        # #Edith enters another line: "Make a fly"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # After upd the page should show both lines
        self.check_for_row_in_list_table('1: Buy some feathers')
        self.check_for_row_in_list_table('2: Make a fly')

        self.fail('Finish the functional test!!!')
