from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def is_on_this_page(self):
        return len(self.driver.find_elements_by_link_text('Checkout »')) > 0

    def open(self):
        assert self.is_on_this_page()
        self.driver.get('https://litecart.stqa.ru/en/checkout')
        return self

    def delete_all_products(self):
        shortcut_li = self.driver.find_element_by_css_selector('ul.shortcuts > li')
        shortcut_li.click()
        for i in range(len(self.driver.find_elements_by_css_selector('ul.shortcuts > li'))):
            self.delete_product()

    def delete_product(self):
        table = self.driver.find_elements_by_css_selector('#checkout-summary-wrapper tr')[1]
        self.driver.find_element_by_name('remove_cart_item').click()
        self.wait.until(EC.staleness_of(table))

    def is_any_product_in_cart(self):
        return len(self.driver.find_elements_by_css_selector('ul.shortcuts > li')) > 0
