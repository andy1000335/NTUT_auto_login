import requests
import time

for i in range(1000):
    source = 'https://nportal.ntut.edu.tw/authImage.do'
    response = requests.get(source)
    with open('C:/Users/USER/Desktop/TensorFlow/MyProect/NTUT_Protal/data/'+str(i)+'.jpg','wb') as f:
        f.write(response.content)
    time.sleep(30)