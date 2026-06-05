"""
购物车模块测试用例

测试覆盖：添加商品、批量添加、移除商品、购物车徽标计数、持久化验证
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def login(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )


class TestCart:

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_single_item_to_cart(self, driver):
        """TC-CART-001：添加一件商品，验证购物车徽标变为 1，商品出现在购物车中"""
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()

        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1", f"购物车徽标应为 1，实际: {badge.text}"

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 1

    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_items(self, driver):
        """TC-CART-002：添加 3 件商品，验证购物车数量正确"""
        buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
        for i in range(3):
            buttons[i].click()

        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "3"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_item_from_cart(self, driver):
        """TC-CART-003：添加后移除商品，验证购物车清空"""
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )

        driver.find_element(By.CLASS_NAME, "cart_button").click()
        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 0

    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_persists_after_navigation(self, driver):
        """TC-CART-004：添加商品后浏览其他页，返回验证购物车数量不变"""
        # 添加商品
        driver.find_element(By.CLASS_NAME, "btn_inventory").click()
        # 进入详情页
        driver.find_element(By.CLASS_NAME, "inventory_item_name").click()
        # 返回列表页
        driver.find_element(By.ID, "back-to-products").click()

        badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert badge.text == "1", "购物车内容应在页面跳转后保持"

    @pytest.mark.regression
    @pytest.mark.cart
    def test_continue_shopping(self, driver):
        """TC-CART-005：从购物车点"继续购物"，验证返回商品列表"""
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "continue-shopping"))
        )
        driver.find_element(By.ID, "continue-shopping").click()

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )
        assert "inventory" in driver.current_url