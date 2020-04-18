import tensorflow as tf
import numpy as np
import cv2
import os
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

pwd = os.path.abspath('.')

def predictVerificationCode():
    originImage = Image.open('captcha.png')

    # 圖片前處理
    image = np.asarray(originImage)

    image = image.astype('uint8')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = np.asarray(image)
    image[image>=image[0, :]-5] = 255
    image[image>=image[-1, :]-5] = 255

    image = image * 1.7
    image[image>255] = 255.0
    image[image<255] = 0

    image = image.astype('uint8')
    image = cv2.fastNlMeansDenoising(image, None, 65, 7, 21)
    image = cv2.resize(image,(120, 40), interpolation=cv2.INTER_NEAREST)
    image[image>230] = 255
    image[image<255] = 0

    image = image.astype(float)        # dtype uint8 to float
    image = image / 255.0              # 0 to 1
    image = np.subtract(image, 0.5)    # -0.5 to 0.5
    image = np.multiply(image, 2.0)    # -1 to 1

    image = image[np.newaxis, :, :]

    predict = ''

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    tf.keras.backend.set_session(tf.Session(config=config))

    saver = tf.train.import_meta_graph(pwd + '/save_model/model.ckpt.meta')
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint(pwd + '/save_model/'))

        x = sess.graph.get_tensor_by_name('input:0')
        drop = sess.graph.get_tensor_by_name('dropout:0')

        pred0 = sess.run(sess.graph.get_tensor_by_name('pred0:0'), {x:image, drop:1})
        pred0 = np.argmax(pred0, axis=1)
        predict += chr(pred0 + 65)

        pred1 = sess.run(sess.graph.get_tensor_by_name('pred1:0'), {x:image, drop:1})
        pred1 = np.argmax(pred1, axis=1)
        predict += chr(pred1 + 65)

        pred2 = sess.run(sess.graph.get_tensor_by_name('pred2:0'), {x:image, drop:1})
        pred2 = np.argmax(pred2, axis=1)
        predict += chr(pred2 + 65)

        pred3 = sess.run(sess.graph.get_tensor_by_name('pred3:0'), {x:image, drop:1})
        pred3 = np.argmax(pred3, axis=1)
        predict += chr(pred3 + 65)

    return predict


print('Opening Browser ...')
driver = webdriver.Chrome(ChromeDriverManager().install())    # 使用Chrome
driver.maximize_window()    # 全螢幕顯示
driver.get('https://nportal.ntut.edu.tw/index.do')    # 開啟NTUT入口網站

driver.implicitly_wait(20)


with open(pwd + r'\scaling_ratio.txt', 'r') as f:
    scalingRatio = float(f.read())    # 電腦顯示器縮放比例
    # selenium 以 location 獲取座標為顯示器100%所取得的
    # selenium 截圖是根據電腦顯示器縮放比例

with open(pwd + r'\user.txt', 'r') as f:
    account = f.readline().strip()
    password = f.readline().strip()


# 儲存驗證碼圖片
def save_captcha():
    driver.save_screenshot('captcha.png')
    element = driver.find_element_by_xpath("//img[@id='authImage']")
    left = element.location['x'] * scalingRatio
    top = element.location['y'] * scalingRatio
    right = (element.location['x'] + element.size['width']) * scalingRatio
    bottom = (element.location['y'] + element.size['height']) * scalingRatio

    im = Image.open('captcha.png') 
    im = im.crop((left, top, right, bottom))
    im.save('captcha.png')

import time

print('Predicting ...')
save_captcha()
predict = predictVerificationCode()

driver.find_element_by_xpath("//input[@id='muid']").send_keys(account)
driver.find_element_by_xpath("//input[@id='mpassword']").send_keys(password)
driver.find_element_by_xpath("//input[@id='authcode']").send_keys(predict)
time.sleep(1)
ActionChains(driver).click(driver.find_element_by_xpath("//input[@type='submit']")).perform()

while(driver.current_url == 'https://nportal.ntut.edu.tw/login.do'):
    print('Loging failed ...')
    time.sleep(2)
    ActionChains(driver).click(driver.find_element_by_xpath("//input[@type='button']")).perform()
    driver.implicitly_wait(3)

    save_captcha()
    predict = predictVerificationCode()

    driver.find_element_by_xpath("//input[@id='muid']").send_keys(account)
    driver.find_element_by_xpath("//input[@id='mpassword']").send_keys(password)
    driver.find_element_by_xpath("//input[@id='authcode']").send_keys(predict)
    time.sleep(1)
    ActionChains(driver).click(driver.find_element_by_xpath("//input[@type='submit']")).perform()
