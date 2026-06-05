"""
下单流程测试用例（端到端）

测试覆盖：完整下单流程、必填字段校验、取消订单、金额校验
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def setup(driver, base_url):
    """登录并添加 2 件商品到购物车"""
    driver.get(base_url)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
    )
    # 添加 2 件商品
    buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    buttons[0].click()
    buttons[1].click()
    # 进入购物车
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "checkout"))
    )


class TestCheckout:

    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_complete_checkout_flow(self, driver):
        """TC-CHK-001：完整下单流程，验证成功页面"""
        driver.find_element(By.ID, "checkout").click()

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        driver.find_element(By.ID, "first-name").send_keys("陈")
        driver.find_element(By.ID, "last-name").send_keys("慧")
        driver.find_element(By.ID, "postal-code").send_keys("518000")
        driver.find_element(By.ID, "continue").click()

        # 确认页 — 验证金额和商品
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text = driver.find_element(By.CLASS_NAME, "summary_total_label").text
        assert "Total" in total_text

        driver.find_element(By.ID, "finish").click()

        # 完成页
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        assert "THANK YOU" in driver.find_element(By.CLASS_NAME, "complete-header").text.upper()

    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_missing_first_name(self, driver):
        """TC-CHK-002：缺姓，验证错误提示"""
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "continue"))
        )
        driver.find_element(By.ID, "last-name").send_keys("慧")
        driver.find_element(By.ID, "postal-code").send_keys("518000")
        driver.find_element(By.ID, "continue").click()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "First Name is required" in error.text

    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_cancel(self, driver):
        """TC-CHK-003：取消下单，验证返回购物车且商品仍在"""
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "cancel"))
        )
        driver.find_element(By.ID, "cancel").click()

        cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_items) == 2, "取消后购物车应保留 2 件商品"

    @pytest.mark.regression
    @pytest.mark.checkout
    def test_checkout_total_calculation(self, driver):
        """TC-CHK-004：验证总金额 = 商品金额 + 税"""
        driver.find_element(By.ID, "checkout").click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )
        driver.find_element(By.ID, "first-name").send_keys("陈")
        driver.find_element(By.ID, "last-name").send_keys("慧")
        driver.find_element(By.ID, "postal-code").send_keys("518000")
        driver.find_element(By.ID, "continue").click()

        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_subtotal_label"))
        )

        subtotal = float(
            driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
            .text.replace("Item total: $", "")
        )
        tax = float(
            driver.find_element(By.CLASS_NAME, "summary_tax_label")
            .text.replace("Tax: $", "")
        )
        total = float(
            driver.find_element(By.CLASS_NAME, "summary_total_label")
            .text.replace("Total: $", "")
        )

        assert abs(total - (subtotal + tax)) < 0.01, (
            f"金额不匹配: subtotal=${subtotal}, tax=${tax}, total=${total}"
        )