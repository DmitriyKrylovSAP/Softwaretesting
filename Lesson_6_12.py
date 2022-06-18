import os
import time
import faker
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_all_chapter(driver):
    fake = faker.Faker('en_US')
    # авторизация в админке
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    driver.get("http://localhost/litecart/admin/?category_id=0&app=catalog&doc=edit_product ")
    # заполнение вкладки general
    driver.find_element_by_xpath("//input[@value = 1 and @type = 'radio']").click()
    product = "Duck for " + fake.first_name()
    driver.find_element_by_xpath("//*[@name = 'name[en]']").send_keys(product)
    driver.find_element_by_xpath("//*[@name = 'code']").send_keys(fake.pyint(5))
    driver.find_element_by_xpath("//input[@data-name = 'Root']").click()
    driver.find_element_by_xpath("//input[@data-name = 'Rubber Ducks']").click()
    driver.find_element_by_xpath("//*[@name = 'quantity']").send_keys(10)
    driver.find_element_by_xpath("//*[@name = 'new_images[]']").send_keys(os.getcwd()+"/test_duck.jpeg")
    driver.find_element_by_xpath("//*[@name = 'date_valid_from']").send_keys("02.02.2022")
    driver.find_element_by_xpath("//*[@name = 'date_valid_to']").send_keys("02.02.2022")
    # заполнение вкладки Information
    driver.find_element_by_xpath("//*[text()='Information']").click()
    driver.find_element_by_xpath("//*[@name = 'short_description[en]']").send_keys(fake.text(10))
    driver.find_element_by_xpath("//*[@class = 'trumbowyg-editor']").send_keys(fake.text(100))
    # заполнение вкладки Prices
    driver.find_element_by_xpath("//*[text()='Prices']").click()
    driver.find_element_by_xpath("//*[@name = 'purchase_price']").send_keys(1)
    driver.find_element_by_xpath("//*[@name = 'prices[USD]']").send_keys(20)
    driver.find_element_by_xpath("//*[@name = 'save']").click()
    # ожидание полной загрузки
    time.sleep(3)
    # проверка уведомления и наличия товара
    driver.find_element_by_css_selector(".notice.success")
    driver.find_element_by_link_text(product)
