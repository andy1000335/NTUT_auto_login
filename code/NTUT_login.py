from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import os
from PIL import Image
import verificationCode_identification as vci
from bs4 import BeautifulSoup
import requests


driver = webdriver.Chrome(ChromeDriverManager().install())    # 使用Chrome
driver.maximize_window()    # 全螢幕顯示

driver.get('https://nportal.ntut.edu.tw/index.do')    # 開啟NTUT入口網站

driver.implicitly_wait(20)


with open(os.path.abspath('.') + r'\scaling_ratio.txt', 'r') as f:
    scalingRatio = float(f.read())    # 電腦顯示器縮放比例
    # selenium 以 location 獲取座標為顯示器100%所取得的
    # selenium 截圖是根據電腦顯示器縮放比例

with open(os.path.abspath('.') + r'\user.txt', 'r') as f:
    account = f.readline().strip()
    password = f.readline().strip()


# 儲存驗證碼圖片
def save_captcha():
    driver.save_screenshot(os.path.abspath('.') + r'\captcha.png')
    element = driver.find_element_by_xpath("//img[@id='authImage']")
    left = element.location['x'] * scalingRatio
    top = element.location['y'] * scalingRatio
    right = (element.location['x'] + element.size['width']) * scalingRatio
    bottom = (element.location['y'] + element.size['height']) * scalingRatio

    im = Image.open(os.path.abspath('.') + r'\captcha.png') 
    im = im.crop((left, top, right, bottom))
    im.save(os.path.abspath('.') + r'\captcha.png')

import time

save_captcha()
predict = vci.predictVerificationCode()

driver.find_element_by_xpath("//input[@id='muid']").send_keys(account)
driver.find_element_by_xpath("//input[@id='mpassword']").send_keys(password)
driver.find_element_by_xpath("//input[@id='authcode']").send_keys(predict)

time.sleep(1)
ActionChains(driver).click(driver.find_element_by_xpath("//input[@type='submit']")).perform()

while(driver.current_url == 'https://nportal.ntut.edu.tw/login.do'):
    time.sleep(2)
    ActionChains(driver).click(driver.find_element_by_xpath("//input[@type='button']")).perform() # error
    driver.implicitly_wait(10)

    save_captcha()
    predict = vci.predictVerificationCode()
    driver.find_element_by_xpath("//input[@id='muid']").send_keys(account)
    driver.find_element_by_xpath("//input[@id='mpassword']").send_keys(password)
    driver.find_element_by_xpath("//input[@id='authcode']").send_keys(predict)
    time.sleep(1)
    ActionChains(driver).click(driver.find_element_by_xpath("//input[@type='submit']")).perform()

ActionChains(driver).click(driver.find_element_by_xpath("//*[@id='divStandaptree']/ul/li[2]/a")).perform()
ActionChains(driver).click(driver.find_element_by_xpath("//*[@id='ap-aa']/ul/li[8]/span/a")).perform()
