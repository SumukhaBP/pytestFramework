import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",action="store",default="chrome"
    )

@pytest.fixture(scope="class")
def setup(request):
    browser_name = request.config.getoption("browser_name")
    print(browser_name)
    service_obj = Service("E:/Pycharm_selenium/Chrome_driver/chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj)
    driver.maximize_window()
    driver.get("http://dev.smartmedsolution.com/login")
    driver.implicitly_wait(20)
    request.cls.driver = driver
    yield
    driver.close()