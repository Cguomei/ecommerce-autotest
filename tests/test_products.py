"""
商品模块测试用例

测试覆盖：商品列表加载、排序功能、商品详情页、图片加载
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


@pytest.fixture(autouse=True)
def login(driver, base_url):
    """每个测试前自动登录"""
    driver.get(base_url)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )


class TestProducts:

    @pytest.mark.smoke
    def test_product_list_display(self, driver):
        """TC-PROD-001：商品列表正常加载，至少显示 1 件商品"""
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) > 0, "商品列表为空"
        # 每件商品应有名称、价格、图片、加入购物车按钮
        for item in items:
            assert item.find_element(By.CLASS_NAME, "inventory_item_name").text
            assert item.find_element(By.CLASS_NAME, "inventory_item_price").text
            assert item.find_element(By.CLASS_NAME, "btn_inventory").is_displayed()

    @pytest.mark.regression
    def test_sort_price_low_to_high(self, driver):
        """TC-PROD-002：按价格从低到高排序，验证价格递增"""
        sort_select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_select.select_by_value("lohi")

        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        price_values = [float(p.text.replace("$", "")) for p in prices]
        assert price_values == sorted(price_values), f"价格未按升序排列: {price_values}"

    @pytest.mark.regression
    def test_sort_name_a_to_z(self, driver):
        """TC-PROD-003：按名称 A-Z 排序，验证字母顺序"""
        sort_select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_select.select_by_value("az")

        names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        name_texts = [n.text for n in names]
        assert name_texts == sorted(name_texts), f"名称未按字母排序: {name_texts}"

    @pytest.mark.regression
    def test_product_detail_page(self, driver):
        """TC-PROD-004：点击商品进入详情页，验证信息一致"""
        first_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        first_item_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

        driver.find_element(By.CLASS_NAME, "inventory_item_name").click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_details_name"))
        )
        detail_name = driver.find_element(By.CLASS_NAME, "inventory_details_name").text
        detail_price = driver.find_element(By.CLASS_NAME, "inventory_details_price").text

        assert detail_name == first_item_name, f"详情页名称不匹配: {detail_name} != {first_item_name}"
        assert detail_price == first_item_price, f"详情页价格不匹配: {detail_price} != {first_item_price}"
        assert driver.find_element(By.CLASS_NAME, "btn_inventory").is_displayed()

    @pytest.mark.regression
    def test_product_images_loaded(self, driver):
        """TC-PROD-005：所有商品图片正常加载（非空 src）"""
        images = driver.find_elements(By.CLASS_NAME, "inventory_item_img")
        for i, img in enumerate(images):
            src = img.get_attribute("src")
            assert src and src.startswith("http"), f"第 {i+1} 件商品图片加载失败"