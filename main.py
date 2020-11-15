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
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    apps_ul = driver.find_element_by_id("box-apps-menu")
    apps_links = []
    for app in apps_ul.find_elements_by_id("app-"):
        apps_links.append(app.find_element_by_css_selector("a").get_attribute("href"))
    for app_link in apps_links:
        driver.find_element_by_css_selector(f"a[href='{app_link}']").click()
        find_h1(driver)
        for i in range(1, len(driver.find_elements_by_css_selector("#app-.selected li"))):
            driver.find_element_by_css_selector(f"#app-.selected li:nth-child({i+1})").click()
            find_h1(driver)

