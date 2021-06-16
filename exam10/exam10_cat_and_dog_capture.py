import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import cv2
import time

# form_window는 하나의 클래스
# 생성한 window를 클래스로 만들어줌
form_window = uic.loadUiType('./mainWidget.ui')[0]

# 생성자 함수
class Exam(QWidget, form_window):
    def __init__(self):
        # super를 사용하면 상위 클래스까지 함께 출력
        # __init__을 사용했을 경우에만!
        super().__init__()
        self.path = None
        self.setupUi(self)
        # 예측 모델 불러오기
        self.model = load_model('../models/cat_and_dog_binary_classification.h5')

        # 버튼 클릭 시 이미지 분류 함수 실행
        self.btn_select.clicked.connect(self.predict_image)

    # 버튼 누르면 실행될 함수
    def predict_image(self):
        # cv2를 이용하여 비디오 캡쳐 객체 생성
        capture = cv2.VideoCapture(0)
        # 출력 이미지 크기 설정
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        flag = True
        while flag:
            ret, frame = capture.read()
            cv2.imshow("VideoFrame", frame)
            time.sleep(0.5)
            print('capture')
            cv2.imwrite('./imgs/capture.png', frame)

            # key 입력 받아 종료
            key = cv2.waitKey(33)
            if key == 27:
                flag = False

            pixmap = QPixmap('./imgs/capture.png') # 이미지 읽어오기
            self.lbl_image.setPixmap(pixmap)

            try:
                img = Image.open('./imgs/capture.png')
                img = img.convert('RGB')
                img = img.resize((64, 64))
                data = np.asarray(img)
                data = data / 255
                data = data.reshape(1, 64, 64, 3)

            except:
                print('error')
            predict_value = self.model.predict(data)
            if predict_value > 0.5:
                # 문자열 출력은 setText함수
                self.lbl_predict.setText('이 이미지는 ' +
                    str((predict_value[0][0] * 100).round()) + '% 확률로 Dog입니다')
            else:
                self.lbl_predict.setText('이 이미지는 ' +
                    str(((1 - predict_value[0][0]) * 100).round()) + '% 확률로 Cat입니다')
        capture.release()
        cv2.destroyAllWindows()

# 프로그램을 만들기 위한 객체 생성
app = QApplication(sys.argv) # sys.argv는 py파일의 절대경로 (QApplication 객체가 실행할 파일이 현재 파이썬 코드라는 것을 알려줌)
mainWindow = Exam()
mainWindow.show()
# 프로그램을 무한 루프 상태로 만듦
sys.exit(app.exec_())