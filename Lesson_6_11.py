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
    driver.get("http://localhost/litecart/en/create_account")
    # регистрация
    fake = faker.Faker('en_US')
    fake_phone = fake.bothify(text='+168########')
    driver.find_element_by_name("phone").send_keys(fake_phone)
    driver.find_element_by_name("firstname").send_keys(fake.first_name())
    driver.find_element_by_name("lastname").send_keys(fake.last_name())
    driver.find_element_by_name("address1").send_keys(fake.city())
    driver.find_element_by_name("postcode").send_keys(fake.postcode())
    driver.find_element_by_name("city").send_keys(fake.city())
    passw = fake.pyint(8)
    mail = fake.email()
    driver.find_element_by_name("email").send_keys(mail)
    driver.find_element_by_name("password").send_keys(passw)
    driver.find_element_by_name("confirmed_password").send_keys(passw)
    driver.find_element_by_class_name("select2-selection__arrow").click()
    driver.find_element_by_class_name("select2-search__field").send_keys("United States")
    driver.find_element_by_class_name("select2-search__field").send_keys(Keys.ENTER)
    time.sleep(1)
    # не уверен, стоит ли кликать на селект
    driver.find_element_by_xpath("//select[@name = 'zone_code']").click()
    driver.find_element_by_xpath("//*[text()='Alaska']").click()
    driver.find_element_by_name("create_account").click()
    # выход
    driver.find_element_by_xpath("//*[text()='Logout']").click()
    driver.find_element_by_name("email").send_keys(mail)
    driver.find_element_by_name("password").send_keys(passw)
    # вход
    driver.find_element_by_xpath("//*[@name='login']").click()
    # выход
    driver.find_element_by_xpath("//*[text()='Logout']").click()


