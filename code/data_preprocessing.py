import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread(r'C:\Users\USER\Desktop\TensorFlow\MyProect\NTUT_Protal\data\LAMP.jpg')

# 灰階
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.subplot(221),plt.imshow(img, cmap='gray')

# 去背
img = np.array(img)
img[img>=img[0, :]-5]=255     # 比第一列顏色還淺的都變成白色
img[img>=img[-1, :]-5]=255    # 比最後一列顏色還淺的都變成白色
plt.subplot(222),plt.imshow(img, cmap='gray')

# 增加對比
img = img * 1.8
img[img>255]=255
img[img<255]=0   # 二值化
plt.subplot(223),plt.imshow(img, cmap='gray')

# 降噪
img = img.astype('uint8')
img = cv2.fastNlMeansDenoising(img, None, 65, 7, 21)
img[img>230]=255    # 二值化
img[img<255]=0
plt.subplot(224),plt.imshow(img, cmap='gray')

plt.show()