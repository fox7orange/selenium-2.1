import pytest
from selenium import webdriver
import os
import datetime
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def fill_gapes_general(driver):
    driver.find_element_by_name('name[en]').send_keys('New auto product')
    driver.find_element_by_name('code').send_keys(f'{datetime.datetime.now().timestamp()}'.replace('.', ''))
    driver.find_element_by_css_selector('input[name="product_groups[]"][value="1-3"]').click()
    driver.find_element_by_css_selector('input[name="quantity"]').clear()
    driver.find_element_by_css_selector('input[name="quantity"]').send_keys('100')
    driver.find_element_by_name('new_images[]').send_keys(os.path.abspath('pic.png'))
    driver.find_element_by_name('date_valid_from').send_keys('11112020')


def fill_gapes_information(driver):
    # man_select = Select(driver.find_element_by_css_selector('select[name="manufacturer_id"]'))
    man_select = Select(WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'select[name="manufacturer_id"]'))))
    man_select.select_by_index(1)
    driver.find_element_by_name('keywords').send_keys('new product buy')
    driver.find_element_by_name('short_description[en]').send_keys('really new auto created product')
    driver.find_element_by_name('head_title[en]').send_keys('NEW!')


def fill_gapes_prices(driver):
    price = driver.find_element_by_name('purchase_price')
    price.clear()
    price.send_keys('100')
    price_cur_code = Select(driver.find_element_by_name('purchase_price_currency_code'))
    price_cur_code.select_by_visible_text('Euros')


def fill_gapes(driver):
    fill_gapes_general(driver)
    driver.find_element_by_class_name('tabs').find_element_by_link_text('Information').click()
    fill_gapes_information(driver)
    driver.find_element_by_class_name('tabs').find_element_by_link_text('Prices').click()
    fill_gapes_prices(driver)


def test_windows(driver):
    driver.implicitly_wait(5)
    wdw = WebDriverWait(driver, 5)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    time.sleep(1)
    driver.find_element_by_link_text('Add New Country').click()
    links = driver.find_elements_by_class_name('fa-external-link')
    for link in links:
        cur_window = driver.current_window_handle
        windows_now_opened = set(driver.window_handles)
        link.click()
        wdw.until(EC.new_window_is_opened(windows_now_opened))
        driver.switch_to_window((set(driver.window_handles)-windows_now_opened).pop())
        driver.close()
        driver.switch_to_window(cur_window)

