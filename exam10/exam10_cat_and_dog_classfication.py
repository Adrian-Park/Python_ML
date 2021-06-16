import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

X_train, X_test, Y_train, Y_test = np.load('../datasets/binary_image_data.npy',
                                           allow_pickle = True) # 원래의 타입 그대로 읽어옴
print('X_train shape : ', X_train.shape)
print('X_test shape : ', X_test.shape)
print('Y_train shape : ', Y_train.shape)
print('Y_test shape : ', Y_test.shape)

# 모델 생성

model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), input_shape=(64,64,3), padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))  # ==> 32 (32,32)

model.add(Conv2D(32, kernel_size=(3,3), padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))  # ==> 16 (16,16)

model.add(Conv2D(64, kernel_size=(3,3), padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=(2,2)))  # ==> 8 (8,8)
model.add(Dropout(0.25))

model.add(Flatten())

model.add(Dense(256, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])

# # early_stopping 설정
# early_stopping = EarlyStopping(monitor='val_accuracy', patience=7) # val_accuracy가 7epochs 동안 증가하지 않으면 멈춤
#
# model.summary()
#
# # 모델 학습
# fit_hist = model.fit(X_train, Y_train, batch_size=64, epochs=100, validation_split=0.15, callbacks=[early_stopping])
#
# # 모델 저장
# model.save('../models/cat_and_dog_binary_classfication.h5')
#
# # 검증 정확도 확인
# score = model.evaluate(X_test, Y_test)
# print('Evaluation loss : ', score[0])
# print('Evaluation accuracy : ', score[1])
#
# # plt 찍어보기
# plt.plot(fit_hist.history['loss'], label='loss')
# plt.plot(fit_hist.history['val_loss'], label='val_loss')
# plt.legend()
# plt.show()
#
# plt.plot(fit_hist.history['accuracy'], label='accuracy')
# plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
# plt.legend()
# plt.show()

early_stopping = EarlyStopping(monitor='val_accuracy', patience=7)  # validation중 epoch:7까지 좋아지지 않으면 멈준다.
model.summary()

fit_hist = model.fit(X_train, Y_train, batch_size=64, epochs=100, validation_split=0.15, callbacks=[early_stopping])

model.save('../models/cat_and_dog_binary_classification.h5') # h5로 해야 불러다가 쓸수있는 파일로 저장된다.
score = model.evaluate(X_test, Y_test)

print('Evaluation loss :', score[0])
print('Evaluation accuracy :', score[1])

plt.plot(fit_hist.history['loss'], label='loss')
plt.plot(fit_hist.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()