from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def open(self, link: str):
        self.driver.get(link)
        return self

    def get_first_product_link(self):
        return self.driver.find_element_by_class_name('.product > a').get_attribute('href')

    def get_number_of_products_in_cart(self):
        return int(self.driver.find_element_by_css_selector('#cart span.quantity').text)

    def product_to_cart(self):
        try:
            size_select = Select(self.driver.find_element_by_name('options[Size]'))
        except NoSuchElementException:
            size_select = False
        if size_select:
            size_select.select_by_index(1)
        self.driver.find_element_by_name("add_cart_product").click()
        num_products_in_cart = self.get_number_of_products_in_cart()
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart span.quantity'),
                                                         str(num_products_in_cart+1)))
