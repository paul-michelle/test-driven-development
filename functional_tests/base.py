import os
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10
SLEEP_TIME = 0.5


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = f'http://{staging_server}'
        # self.browser.implicitly_wait(3)

    def tearDown(self) -> None:
        self.browser.quit()

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

    @staticmethod
    def wait_for(fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (WebDriverException, AssertionError) as e:
                time_elapsed = time.time() - start_time
                if time_elapsed > MAX_WAIT:
                    raise e
                time.sleep(SLEEP_TIME)

