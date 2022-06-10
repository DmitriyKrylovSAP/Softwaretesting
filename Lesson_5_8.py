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
    countrie_with_zone = []
    #перебираем все строки
    for countrie in countries:
        # поиск первой буквы названи страны и перевод в нижний регистр
        countrie_letter = countrie.find_element_by_xpath(".//a").get_attribute("text")[0].lower()
        #  составляем список стран с зонами
        if int(countrie.find_element_by_xpath(".//td[6]").get_attribute("innerText")) != 0:
            countrie_with_zone.append(countrie.find_element_by_xpath(".//a").get_attribute("text"))
        # проверка того, что страны идут по порядку
        assert countrie_letter_sample <= countrie_letter
        countrie_letter_sample = countrie_letter

    #  ищем название страны с поиске и проверяем зоны в ней
    for countrie_zone in countrie_with_zone:
        countries = driver.find_elements_by_xpath("//*[@name='countries_form']//*[@class='row']")
        for countrie in countries:
            if countrie.find_element_by_xpath(".//a").get_attribute("text") == countrie_zone:
                countrie.find_element_by_xpath(".//a").click()
                zone = driver.find_elements_by_xpath("//*[@id='table-zones']//*[contains(@name, '[name]')]")
                zone_letter_sample = "a"
                for zone_name in zone:
                    # проверяем что название зоны не пустое
                    if len(zone_name.find_element_by_xpath("./..").get_attribute("innerText")) > 0:
                        zone_letter = str(zone_name.find_element_by_xpath("./..").get_attribute("innerText")[0]).lower()
                        assert zone_letter_sample <= zone_letter
                        zone_letter_sample = zone_letter
                break
        driver.back()


