from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self,driver):
        self.driver = driver
    username = (By.NAME,"username")
    password = (By.ID,"password")
    loginButton = (By.XPATH,"//button[text()='Login']")

    def userName(self):
        return self.driver.find_element(*LoginPage.username)
    def passWord(self):
        return self.driver.find_element(*LoginPage.password)
    def logButton(self):
        return self.driver.find_element(*LoginPage.loginButton)
