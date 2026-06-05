"""
登录模块测试用例

测试覆盖：正常登录、错误密码、空凭证、锁定用户、页面UI验证
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_success(self, driver, base_url):
        """TC-LOGIN-001：标准用户正常登录，验证跳转到商品列表页"""
        driver.get(base_url)
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert "inventory" in driver.current_url
        assert driver.find_element(By.CLASS_NAME, "title").text == "Products"

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_wrong_password(self, driver, base_url):
        """TC-LOGIN-002：错误密码登录，验证显示错误提示"""
        driver.get(base_url)
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("wrong_password")
        driver.find_element(By.ID, "login-button").click()

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "Username and password do not match" in error.text

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_empty_credentials(self, driver, base_url):
        """TC-LOGIN-003：空用户名密码，验证错误提示"""
        driver.get(base_url)
        driver.find_element(By.ID, "login-button").click()
        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "Username is required" in error.text

    @pytest.mark.regression
    @pytest.mark.login
    def test_login_locked_out_user(self, driver, base_url):
        """TC-LOGIN-004：锁定用户登录，验证锁定提示"""
        driver.get(base_url)
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        assert "locked out" in error.text.lower()

    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_ui(self, driver, base_url):
        """TC-LOGIN-005：登录页 UI 完整性检查"""
        driver.get(base_url)
        assert driver.find_element(By.ID, "user-name").is_displayed()
        assert driver.find_element(By.ID, "password").is_displayed()
        assert driver.find_element(By.ID, "login-button").is_displayed()
        assert "Swag Labs" in driver.title