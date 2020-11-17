import pytest
from selenium import webdriver


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


def test_10(driver):
    main_params = get_main_page_params(driver)
    product_params = get_product_page_params(driver)
    assert main_params[0] == product_params[0]
    assert main_params[1] == product_params[1]
    assert main_params[2] == product_params[2]
    assert main_params[3] and product_params[3]
    assert main_params[4] and product_params[4]
    assert main_params[5] and product_params[5]
