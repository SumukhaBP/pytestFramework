import json
import logging
import time

import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# from pageObject.LoginPage import LoginPage
# from utilities.BaseClass import BaseClass
with open("E:/Pycharm_selenium/Json/abdo_table.json",'r') as file:
    json_data = json.load(file)
@pytest.mark.usefixtures("setup")
class BaseClass:
    def getLogger(self):
        logger = logging.getLogger(__name__)

        fileHandler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s :%(funcName)s : %(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)

        logger.setLevel(logging.DEBUG)
        return logger

class WoksheetPage:
    def __init__(self,driver,log):
        self.driver = driver
        self.log = log

    def fill_size_input(self,struct_name):
        size_inputs = self.driver.find_elements(By.XPATH,
                                           "//tr[@note-structure='{}']//input[@type='text']".format(struct_name))
        for size in size_inputs:
            size.send_keys('12')

    def table_fill_data(self,path, data, input_elem):
        for tdata in data:
            time.sleep(2)
            print(
                input_elem + "//span[text()='{}']//parent::label//parent::div//parent::div//parent::td//following-sibling::td//span[text()='{}']".format(
                    tdata, data[tdata]))
            if tdata == "number":
                self.driver.find_element(By.XPATH, input_elem + "//span[text()='{}']".format(data[tdata])).click()
            elif tdata == "Size":
                self.driver.find_element(By.XPATH, input_elem + "//input[@type='text']").send_keys(data[tdata])
            else:
                self.driver.find_element(By.XPATH,
                                    input_elem + "//span[text()='{}']//parent::label//parent::div//parent::div//parent::td//following-sibling::td//span[text()='{}']".format(
                                        tdata, data[tdata])).click()

    def fill_worksheet(self,json_data):
        self.log.info("started filling the worksheet")
        for key in json_data:
            print("//tr[@note-structure='{}']//span[text()='{}']".format(key, json_data[key]))
            if key == "Worksheet":
                time.sleep(5)
                self.driver.find_element(By.XPATH, "//tr[@profiletype='{} Ultrasound']//a[text()='Start']".format(
                    json_data[key])).click()
                # driver.find_element(By.CSS_SELECTOR, "#start-new-patient").click()
                # driver.find_element(By.CSS_SELECTOR,"a.pelvic div").click()
                # patient_details()
            elif key == "Clinical Hx":
                self.driver.find_element(By.XPATH,
                                    "//tr[@note-structure='{}']//textarea[@name='history-reporting-textbox']".format(
                                        key)).send_keys(json_data[key])
            elif key == "Technique":
                tech_data = json_data[key]
                for tkey in tech_data:
                    self.driver.find_element(By.XPATH,
                                        "//tr[@note-structure='{}']//span[text()='{}']".format(key, tkey)).click()
                    time.sleep(3)
                    self.driver.find_element(By.XPATH,
                                        "//tr[@note-structure='{}']//span[text()='{}']//parent::label//following-sibling::div//span[text()='{}']".format(
                                            key, tkey, tech_data[tkey])).click()
            elif isinstance(json_data[key],dict):  # type(json_data[key]) == dict:
                time.sleep(3)
                self.driver.find_element(By.XPATH, "//tr[@note-structure='{}']//span[text()='Comments']".format(key)).click()
                comment_data = json_data[key]
                print("---Commets data---")
                self.log.info("comments data",comment_data)
                for cKey in comment_data:
                    if cKey == "Fibroid seen" or cKey == "Cyst" or cKey == "Focal area (Solid/Indeterminate)" or cKey == "Nabothian cyst":
                        if isinstance(comment_data[cKey], dict): #comment_data[cKey] != "No":
                            time.sleep(3)
                            self.driver.find_element(By.XPATH, "//tr[@note-structure='{}']//span[text()='{}']".format(key,
                                                                                                                 cKey)).click()
                            elem = "//tr[@note-structure='{}']//span[text()='{}']//parent::label//following-sibling::div".format(
                                key, cKey)
                            self.table_fill_data(key, comment_data[cKey], elem)
                        else:
                            print("//tr[@note-structure='{}']//span[text()='{}']".format(key, comment_data[cKey]))
                            self.driver.find_element(By.XPATH, "//tr[@note-structure='{}']//span[text()='{}']".format(key,
                                                                                                                 cKey)).click()

                            time.sleep(3)
                            self.driver.find_element(By.XPATH,
                                                "//tr[@note-structure='{}']//span[text()='{}']//parent::label//following-sibling::div//span[text()='{}']".format(
                                                    key, cKey, comment_data[cKey])).click()

                    else:
                        print("//tr[@note-structure='{}']//span[text()='{}']".format(key, comment_data[cKey]))
                        self.driver.find_element(By.XPATH,
                                            "//tr[@note-structure='{}']//span[text()='{}']".format(key, cKey)).click()

                        time.sleep(3)
                        self.driver.find_element(By.XPATH,
                                            "//tr[@note-structure='{}']//span[text()='{}']//parent::label//following-sibling::div//span[text()='{}']".format(
                                                key, cKey, comment_data[cKey])).click()

                    # pathology.find_element(By.XPATH,"//span[text()='{}']".format(comment_data[cKey])).click()

                print("---Commets end---")
                self.log.info("comments end")
            elif key == "Uterus position":
                self.driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
                time.sleep(3)
                # action.double_click(driver.find_element(By.XPATH,"//tr[@note-structure='{}']//span[text()='{}']".format(key,json_data[key]))).perform()
                self.driver.find_element(By.XPATH,
                                    "//tr[@note-structure='{}']//span[text()='{}']".format(key, json_data[key])).click()
            else:
                self.driver.find_element(By.XPATH,
                                    "//tr[@note-structure='{}']//span[text()='{}']".format(key, json_data[key])).click()
            if key in ["Uterus size", "Single wall muscle thickness (transverse image)", "Pylorus length"]:
                self.fill_size_input(key)
            time.sleep(2)

    def preview_com(self):
        self.log.info("completing the worksheet")
        self.driver.find_element(By.XPATH,
                            "//div[@class='col-md-12 nav-top-header sono-header']//button[@id='complete-btn']").click()
        # time.sleep(20)
        self.driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
        print("scroll")
        # time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR,
                            "div[id='screenshot-div'] label[class='checkbox checkbox-styled review-check-img'] span").click()
        # time.sleep(5)
        self.driver.find_element(By.XPATH, "//button[@id='complete-screenshot']").click()

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

class TestGeneralTemp(BaseClass):
    def test_e2e(self):
        log = self.getLogger()
        print("inside test class")
        login_obj = LoginPage(self.driver)
        login_obj.userName().send_keys("demo@medreport360.com")
        # self.driver.find_element(By.NAME, "username").send_keys("demo@medreport360.com")
        login_obj.passWord().send_keys("password123")
        # self.driver.find_element(By.ID, "password").send_keys("password123")
        login_obj.logButton().click()
        log.info("login succefull")
        # self.driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(5)
        worksheet_obj = WoksheetPage(self.driver,log)
        worksheet_obj.fill_worksheet(json_data)
        worksheet_obj.preview_com()