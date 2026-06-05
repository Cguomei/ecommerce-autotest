# 🧪 E-Commerce Automation Test Framework

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green?logo=selenium)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-9.x-orange?logo=pytest)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
[![CI](https://github.com/Cguomei/ecommerce-autotest/actions/workflows/test.yml/badge.svg)](https://github.com/Cguomei/ecommerce-autotest/actions)

基于 **Selenium WebDriver + pytest** 的电商网站自动化测试框架，以 [SauceDemo](https://www.saucedemo.com) 为测试靶场，覆盖登录、商品浏览、购物车、下单四大核心模块。

> 📌 本项目为个人学习实践作品，旨在展示 Web 自动化测试的工程化能力——从用例设计、夹具复用、失败截图到 CI/CD 集成。

## 📋 目录

- [测试覆盖](#-测试覆盖)
- [项目结构](#-项目结构)
- [快速开始](#-快速开始)
- [测试报告](#-测试报告)
- [技术栈](#-技术栈)
- [设计思路](#-设计思路)
- [CI/CD](#-cicd)

## 🧪 测试覆盖

**19 条自动化用例**，按模块和优先级分层：

| 模块 | 用例数 | 覆盖场景 | 标记 |
|------|:------:|----------|------|
| **登录** | 5 | 正常登录、错误密码、空凭证、锁定用户、UI 完整性 | `smoke` `login` |
| **商品** | 5 | 列表加载、价格排序、名称排序、详情页、图片加载 | `smoke` `regression` |
| **购物车** | 5 | 添加/批量/移除商品、徽标计数、跨页面持久化 | `smoke` `cart` |
| **下单** | 4 | 完整下单流程、字段校验、取消订单、金额计算 | `smoke` `checkout` |

### 测试标记策略

| 标记 | 用途 | 运行方式 |
|------|------|----------|
| `@pytest.mark.smoke` | 冒烟测试——核心流程必须通过 | `pytest -m smoke` |
| `@pytest.mark.regression` | 回归测试——完整功能验证 | `pytest -m regression` |
| `@pytest.mark.login` / `cart` / `checkout` | 按模块筛选 | `pytest -m login` |

## 📁 项目结构

```
ecommerce-autotest/
├── .github/workflows/
│   └── test.yml           # GitHub Actions CI（自动运行测试）
├── conftest.py            # pytest 全局夹具：WebDriver 管理 + 失败自动截图
├── pytest.ini             # 配置：标记注册、报告路径、默认参数
├── requirements.txt       # Python 依赖
├── tests/
│   ├── __init__.py
│   ├── test_login.py      # 登录模块（5 条）
│   ├── test_products.py   # 商品模块（5 条）
│   ├── test_cart.py       # 购物车模块（5 条）
│   └── test_checkout.py   # 下单模块（4 条）
└── reports/
    ├── report.html        # pytest-html 测试报告
    └── screenshots/       # 失败用例自动截图
```

## 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/Cguomei/ecommerce-autotest.git
cd ecommerce-autotest

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行冒烟测试（5 条核心用例，约 30 秒）
pytest -m smoke --headless

# 4. 运行全量测试并生成 HTML 报告
pytest --headless

# 5. 查看报告
open reports/report.html      # macOS
start reports/report.html     # Windows
```

## 📊 测试报告

每次运行 `pytest` 后自动生成 `reports/report.html`（自包含 HTML，可直接在浏览器打开）。

**报告包含：**
- 测试结果总览（通过/失败/跳过/错误）
- 每条用例的执行时间和状态
- 失败用例的错误堆栈
- 环境信息（Python 版本、平台、依赖版本）

失败用例自动截图保存在 `reports/screenshots/` 目录。

## 🔧 技术栈

| 组件 | 选型 | 说明 |
|------|------|------|
| 自动化引擎 | **Selenium 4.x** | 行业标准，支持多浏览器 |
| 测试框架 | **pytest 9.x** | 夹具（fixture）、标记、参数化 |
| 报告 | **pytest-html** | 自包含 HTML 报告，无需额外服务 |
| 驱动管理 | **webdriver-manager** | 自动下载匹配的 ChromeDriver |
| CI/CD | **GitHub Actions** | 每次推送自动运行测试 |

## 💡 设计思路

**1. Fixture 分层复用**
`conftest.py` 中定义了 `driver` fixture（函数级别，每次测试自动创建/销毁浏览器），以及通过 `autouse=True` fixture 在购物车/下单测试中自动完成登录，避免重复代码。

**2. 失败即截图**
利用 pytest hook `pytest_runtest_makereport`，测试失败时自动截取当前页面状态，保存在 `reports/screenshots/`——不需要事后复现。

**3. 标记驱动执行**
通过 `@pytest.mark.smoke` / `@pytest.mark.regression` 标记实现分层执行：提交代码时跑冒烟（5 条，30 秒），完整回归跑全量（19 条，2-3 分钟）。

**4. 可扩展架构**
当前使用直接定位器（`By.ID` / `By.CLASS_NAME`），适合 20 条以内的小型项目。规模扩大时可平滑迁移到 Page Object 模式——`conftest.py` 的 fixture 结构已为此预留接口。

## 🔄 CI/CD

项目配置了 [GitHub Actions](.github/workflows/test.yml)，每次推送到 `master` 分支自动：

1. 安装 Python 3.10 + Chrome
2. 安装项目依赖
3. 运行全量 19 条用例
4. 上传测试报告为构建产物

CI 状态徽章显示在 README 顶部，面试时可以直接展示"测试通过了 CI 验证"。

---

**Author:** 陈慧 · [GitHub](https://github.com/Cguomei)