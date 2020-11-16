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


def is_alphabetical(driver, col_num: int):
    rows = driver.find_elements_by_css_selector(".dataTable tr.row")
    names = [row.find_element_by_xpath(f"./td[{col_num}]").text for row in rows]
    for i in range(1, len(names)):
        assert names[i - 1] < names[i]


def test_countries(driver):
    driver.implicitly_wait(2)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    is_alphabetical(driver, 5)


def test_zones(driver):
    driver.implicitly_wait(2)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    rows = driver.find_elements_by_css_selector(".dataTable tr.row")
    not_zero_zones_links = []
    for row in rows:
        zone = row.find_element_by_xpath("./td[6]").text
        if int(zone) > 0:
            not_zero_zones_links.append(row.find_element_by_xpath("./td[5]/a").get_attribute("href"))
    for link in not_zero_zones_links:
        driver.get(link)
        is_alphabetical(driver, 3)


def test_geo_zones(driver):
    driver.implicitly_wait(2)
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    rows = driver.find_elements_by_css_selector(".dataTable tr.row")
    country_links = []
    for row in rows:
        country_links.append(row.find_element_by_xpath("./td[3]/a").get_attribute("href"))
    for link in country_links:
        driver.get(link)
        rows = driver.find_elements_by_css_selector(".dataTable tr:not(.header)")
        names = []
        for row in rows:
            tds = row.find_elements_by_css_selector("td")
            if len(tds) == 4:
                names.append(tds[2].find_element_by_css_selector("option[selected]").text)
        for i in range(1, len(names)):
            assert names[i - 1] < names[i]
