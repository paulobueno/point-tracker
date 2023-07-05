from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_check_fooflyers_list(self):
        # Enters in home page
        self.browser.get('http://localhost:8000')

        # Check that Foo Flyers is listed as one of the teams
        self.assertIn('FooTracker', self.browser.title)

        # Clicks on Foo Flyers
        # Check that it is Foo Flyers' page
