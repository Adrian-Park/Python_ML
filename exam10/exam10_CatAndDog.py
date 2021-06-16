import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np


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
        self.path = QFileDialog.getOpenFileName(
            self,
            "Open file", 'C:\work\python\AI_exam\datasets', # 파일 chooser 기본 경로
            "Image Files(*.jpg);;All (*.*)" # 특정 확장자 파일 검색 필터 ;;은 구분자
        )
        print(self.path) # 함수가 호출해주는 파일 경로 확인, 0번 인덱스에 파일 경로 확인

        # path를 받았을 때만 실행시키기
        if self.path[0]:
            # 파일을 pixmap 형식으로 변환 후 화면에 이미지 표시
            pixmap = QPixmap(self.path[0]) # 생성자 파라미터로 이미지 path 넘김
            self.lbl_image.setPixmap(pixmap)

            try:
                img = Image.open(self.path[0])
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

# 프로그램을 만들기 위한 객체 생성
app = QApplication(sys.argv) # sys.argv는 py파일의 절대경로 (QApplication 객체가 실행할 파일이 현재 파이썬 코드라는 것을 알려줌)
mainWindow = Exam()
mainWindow.show()
# 프로그램을 무한 루프 상태로 만듦
sys.exit(app.exec_())