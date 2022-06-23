import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_all_chapter(driver):
    wait = WebDriverWait(driver, 20)
    # авторизация в админке
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    wait.until(EC.presence_of_element_located((By.ID, "box-login-wrapper")))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait.until(EC.presence_of_element_located((By.NAME, "catalog_form")))
    # открываем все папки
    while len(driver.find_elements_by_class_name("fa-folder")) > 0:
        driver.find_element_by_xpath("//*[@class = 'fa fa-folder']//following-sibling::a").click()
    # получаем список ссылок
    links_url = []
    links = driver.find_elements_by_xpath("//*[img]/a")
    for link in links:
        links_url.append(link.get_attribute("href"))

    # кликаем на каждую ссылку и проверяем что в консоли ничего нет
    for link_url in links_url:
        driver.find_element_by_xpath("//*[@href ='" + link_url + "'and @title]").click()
        wait.until(EC.presence_of_element_located((By.ID, "tab-general")))
        assert len(driver.get_log("browser")) == 0
        driver.execute_script("window.history.go(-1)")
        wait.until(EC.presence_of_element_located((By.NAME, "catalog_form")))













