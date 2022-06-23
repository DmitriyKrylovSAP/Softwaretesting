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
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    wait.until(EC.presence_of_element_located((By.ID, "box-login-wrapper")))
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    wait.until(EC.presence_of_element_located((By.ID, "notices-wrapper")))
    driver.find_element_by_class_name("button").click()
    # получаем id текущего окна
    current_window = driver.current_window_handle
    links = driver.find_elements_by_class_name("fa-external-link")
    # кликаем на каждую найденную ссылку
    for link in links:
        link.click()
        # проверка что появился новый id окна
        assert len(driver.window_handles) > 1
        # находим новое окно и закрываем его
        for handle in driver.window_handles:
            if handle != current_window:
                driver.switch_to.window(handle)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div")))
                driver.close()
                driver.switch_to.window(current_window)









