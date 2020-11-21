import pytest
from selenium import webdriver
import datetime
from selenium.webdriver.support.ui import Select


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def get_font_size(text):
    return float(text.value_of_css_property('font-size').replace('px', ''))


def is_gray_crossed(text):
    color_str = text.value_of_css_property('color').replace(' ', '')
    color = color_str
    for i in color_str:
        if i not in '0123456789,':
            color = color.replace(i, '')
    color = color.split(',')
    text_decoration = text.value_of_css_property('text-decoration')
    return (True if text_decoration.find('line-through') != -1 else False) and color[0] == color[1] and color[1] == color[2]


def is_red_bold(text):
    color_str = text.value_of_css_property('color').replace(' ', '')
    color = color_str
    for i in color_str:
        if i not in '0123456789,':
            color = color.replace(i, '')
    color = color.split(',')
    font_weight = text.value_of_css_property('font-weight')
    return font_weight >= '700' and color[1] == '0' and color[2] == '0'


def get_main_page_params(driver):
    driver.get('http://localhost/litecart/en/')
    campaigns_product = driver.find_element_by_css_selector('#box-campaigns li.product')
    name = campaigns_product.find_element_by_class_name('name')
    price = campaigns_product.find_element_by_class_name('regular-price')
    campaign_price = campaigns_product.find_element_by_class_name('campaign-price')
    return [name.text, price.text, campaign_price.text, is_gray_crossed(price), is_red_bold(campaign_price),
            get_font_size(campaign_price) > get_font_size(price)]


def get_product_page_params(driver):
    driver.get('http://localhost/litecart/en/')
    driver.find_element_by_css_selector('#box-campaigns li.product').click()
    name = driver.find_element_by_css_selector('#box-product h1')
    price = driver.find_element_by_css_selector('.content .information .regular-price')
    campaign_price = driver.find_element_by_css_selector('.content .information .campaign-price')
    return [name.text, price.text, campaign_price.text, is_gray_crossed(price), is_red_bold(campaign_price),
            get_font_size(campaign_price) > get_font_size(price)]


def fill_gapes(driver):
    driver.find_element_by_css_selector('[name="firstname"]').send_keys('Firstname')
    driver.find_element_by_css_selector('[name="lastname"]').send_keys('Lastname')
    driver.find_element_by_css_selector('[name="address1"]').send_keys('address')
    driver.find_element_by_css_selector('[name="postcode"]').send_keys('123456')
    driver.find_element_by_css_selector('[name="city"]').send_keys('City')
    country_select = Select(driver.find_element_by_css_selector('select[name="country_code"]'))
    country_select.select_by_visible_text('United States')
    driver.find_element_by_css_selector('[name="email"]').send_keys(str(datetime.datetime.now().timestamp()) + '@mail.ru')
    driver.find_element_by_css_selector('[name="phone"]').send_keys('+71234567890')
    driver.find_element_by_css_selector('[name="password"]').send_keys('password')
    driver.find_element_by_css_selector('[name="confirmed_password"]').send_keys('password')


def test_10(driver):
    driver.get('http://localhost/litecart/en/')
    driver.find_element_by_link_text("New customers click here").click()
    fill_gapes(driver)
    driver.find_element_by_css_selector('button[type="submit"]').click()