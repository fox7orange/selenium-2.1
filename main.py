import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def find_h1(where):
    where.find_element_by_css_selector("#content h1")


def test_example(driver):
    driver.implicitly_wait(2)
    driver.get("http://localhost/litecart/")
    content = driver.find_element_by_class_name("content")
    for product in content.find_elements_by_css_selector('li.product'):
        stickers = product.find_elements_by_class_name('sticker')
        assert len(stickers) != 1
