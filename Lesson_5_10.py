import time
import ast
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
    driver.get("http://localhost/litecart")
    product = driver.find_element_by_css_selector("#box-campaigns .product.column")
    # -------------------
    # главная страница
    # -------------------
    # запоминаем название и цены
    main_name = product.find_element_by_class_name("name").get_attribute("textContent")

    main_regular_price = product.find_element_by_class_name("regular-price")
    main_regular_price_value = main_regular_price.get_attribute("textContent")
    main_regular_price_size = main_regular_price.value_of_css_property("font-size")
    main_regular_price_color = main_regular_price.value_of_css_property("color")
    main_regular_price_line = main_regular_price.value_of_css_property("text-decoration")

    main_campaign_price = product.find_element_by_class_name("campaign-price")
    main_campaign_price_value = main_campaign_price.get_attribute("textContent")
    main_campaign_price_size = main_campaign_price.value_of_css_property("font-size")
    main_campaign_price_color = main_campaign_price.value_of_css_property("color")
    main_campaign_price_weight = main_campaign_price.value_of_css_property("font-weight")

    # обычная цена зачеркнута
    assert "line-through" in main_regular_price_line
    # обычная цена серая
    r, g, b, a = ast.literal_eval(main_regular_price_color.strip("rgba"))
    assert r == g == b
    # акционная цена красная
    r, g, b, a = ast.literal_eval(main_campaign_price_color.strip("rgba"))
    assert g == b == 0
    # акционная цена жирная
    assert int(main_campaign_price_weight) > 400
    # акционная цена выше обычной
    assert main_campaign_price_size > main_regular_price_size
    product.click()

    # -------------------
    # страница товара
    # -------------------
    # запоминаем название и цены
    product_name = driver.find_element_by_css_selector("#box-product .title").get_attribute("textContent")

    product_regular_price = driver.find_element_by_class_name("regular-price")
    product_regular_price_value = product_regular_price.get_attribute("textContent")
    product_regular_price_size = product_regular_price.value_of_css_property("font-size")
    product_regular_price_color = product_regular_price.value_of_css_property("color")
    product_regular_price_line = product_regular_price.value_of_css_property("text-decoration")

    product_campaign_price = driver.find_element_by_class_name("campaign-price")
    product_campaign_price_value = product_campaign_price.get_attribute("textContent")
    product_campaign_price_size = product_campaign_price.value_of_css_property("font-size")
    product_campaign_price_color = product_campaign_price.value_of_css_property("color")
    product_campaign_price_weight = product_campaign_price.value_of_css_property("font-weight")

    # проверяем соответствие названий и цен
    assert main_name == product_name
    assert main_regular_price_value == product_regular_price_value
    assert main_campaign_price_value == product_campaign_price_value
    # обычная цена зачеркнута
    assert "line-through" in product_regular_price_line
    # обычная цена серая
    r, g, b, a = ast.literal_eval(product_regular_price_color.strip("rgba"))
    assert r == g == b
    # акционная цена красная
    r, g, b, a = ast.literal_eval(product_campaign_price_color.strip("rgba"))
    assert g == b == 0
    # акционная цена жирная
    assert int(product_campaign_price_weight) > 400
    # акционная цена выше обычной
    assert product_campaign_price_size > product_regular_price_size
