import tensorflow as tf
import numpy as np
import random
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# source = 'https://nportal.ntut.edu.tw/authImage.do'
# response = requests.get(source)    # 二進制檔

# originImage = Image.open(BytesIO(response.content))
def predictVerificationCode():
    originImage = Image.open('captcha.png')
    # originImage = originImage.resize((120, 40))

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

    saver = tf.train.import_meta_graph('C:/Users/USER/Desktop/TensorFlow/MyProect/NTUT_Protal/save_model/model.ckpt.meta')
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint('C:/Users/USER/Desktop/TensorFlow/MyProect/NTUT_Protal/save_model/'))

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