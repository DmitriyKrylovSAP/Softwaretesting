import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_all_chapter(driver):
    #открытие админки
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    #получение числа элементов бокового меню
    list_count = len(driver.find_elements_by_xpath("//*[@id='box-apps-menu']/li"))
    list_number = 0
    # перебор элементов бокового меню
    while list_number < list_count:
        list = driver.find_elements_by_xpath("//*[@id='box-apps-menu']/li")
        list[list_number].click()
        # получение числа подэлементов бокового меню
        list_second_count = len(driver.find_elements_by_xpath("//*[@id='box-apps-menu']/li/ul/li"))
        list_second_number = 0
        # перебор подэлементов бокового меню
        while list_second_number < list_second_count:
            list_second = driver.find_elements_by_xpath("//*[@id='box-apps-menu']/li/ul/li")
            list_second[list_second_number].click()
            list_second_number += 1
            # проверка наличия заголовка
            assert driver.find_element_by_xpath("//*[h1]")
        list_number += 1
