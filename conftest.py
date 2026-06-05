"""
pytest 全局配置与夹具

提供：
- driver fixture：自动初始化/销毁 Chrome WebDriver
- 失败自动截图
- 命令行控制 headless 模式
"""

import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Run tests in headless mode (no browser window)"
    )
    parser.addoption(
        "--base-url", action="store", default="https://www.saucedemo.com",
        help="Base URL of the application under test"
    )


@pytest.fixture(scope="function")
def driver(request):
    """创建 Chrome WebDriver 实例，测试结束后自动关闭"""
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 可选：用 Page Load Strategy 加速
    options.page_load_strategy = "eager"

    # 自动下载匹配的 ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = os.path.join(
                os.path.dirname(__file__), "reports", "screenshots"
            )
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)
            driver.save_screenshot(filepath)
