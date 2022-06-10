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
    # авторизация в админке
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    # открытие страницы с геозонами
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    # поиск строки с названием страны
    countries = driver.find_elements_by_xpath("//*[@name='countries_form']//*[@class='row']")
    #  задаем образец буквы для сравнения
    countrie_letter_sample = "a"
    #  перебираем все строки
    for countrie in countries:
        # поиск первой буквы названи страны и перевод в нижний регистр
        countrie_letter = countrie.find_element_by_xpath(".//a").get_attribute("text")[0].lower()
        # проверка того, что страны идут по порядку
        assert countrie_letter_sample <= countrie_letter
        countrie_letter_sample = countrie_letter
