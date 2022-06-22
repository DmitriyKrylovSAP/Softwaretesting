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
    wait = WebDriverWait(driver, 10)  # seconds
    # авторизация в админке
    driver.get("http://localhost/litecart")

    # добавление в корзину первого товара в списке
    cart = 1
    while cart <= 3:
        driver.find_element_by_css_selector(".product").click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "images-wrapper")))
        # если товар с параметрами, то пропускаем его
        if len(driver.find_elements_by_css_selector("td.options")) > 0:
            cart -= 1
        else:
            driver.find_element_by_name("add_cart_product").click()
            # проверка числа товаров корзине
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='quantity' and text() ='" + str(cart) + "']")))
        driver.find_element_by_id("logotype-wrapper").click()
        wait.until(EC.presence_of_element_located((By.ID, "slider-wrapper")))
        cart += 1

    # переход в корзину
    driver.find_element_by_xpath("//a[@href='http://localhost/litecart/en/checkout' and @class = 'link']").click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "td.item")))

    # удаление товаров из корзины
    i = 1
    while i <= 3:
        # если есть одинковые товары, то уменьшаем число повторений
        quantity = int(driver.find_element_by_xpath("//div[@id='order_confirmation-wrapper']//tr[2]/td")
                       .get_attribute("textContent"))
        if quantity > 1:
            i = i + quantity - 1
        element = driver.find_element_by_xpath("//div[@id='order_confirmation-wrapper']//tr[2]/td")
        driver.find_element_by_name("remove_cart_item").click()
        wait.until(EC.staleness_of(element))
        i += 1


