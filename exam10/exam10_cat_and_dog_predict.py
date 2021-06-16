from PIL import Image
from tensorflow.keras.models import load_model
import numpy as np
import glob

model = load_model('../models/cat_and_dog_binary_classification.h5')
print(model.summary())

img_dir = '../datasets/train/'
# 이미지 크기 64X64
image_w = 64
image_h = 64

# 강아지 파일 랜덤하게 읽어오기
dog_files = glob.glob(img_dir + 'dog*.jpg') # 문자열 결합, 파일 이름 리스트
# 랜덤하게 인덱스 생성
dog_sample = np.random.randint(len(dog_files))
# 강아지 이미지 경로 뽑아오기
dog_sample_path = dog_files[dog_sample]

# 고양이 파일 랜덤하게 읽어오기
cat_files = glob.glob(img_dir + 'cat*.jpg') # 문자열 결합, 파일 이름 리스트
# 랜덤하게 인덱스 생성
cat_sample = np.random.randint(len(dog_files))
# 고양이 이미지 경로 뽑아오기
cat_sample_path = cat_files[cat_sample]

# 이미지 파일 경로 출력
print(dog_sample_path)
print(cat_sample_path)

try:
    img = Image.open(dog_sample_path)
    # img.show()
    img = img.convert('RGB')
    img = img.resize((image_w, image_h)) # 튜플로 넘겨주기!!
    data = np.asarray(img) # 데이터 타입 변환
    data = data / 255 # 전처리
    dog_data = data.reshape(1, 64, 64, 3) # reshape

    img = Image.open(cat_sample_path)
    # img.show() # 이미지 출력
    img = img.convert('RGB')
    img = img.resize((image_w, image_h)) # 튜플로 넘겨주기!!
    data = np.asarray(img) # 데이터 타입 변환
    data = data / 255 # 전처리
    cat_data = data.reshape(1, 64, 64, 3) # reshape
except:
    print('error')
print(data.shape)

# 예측률 확인 dog data = 1 / cat data = 0
print('dog data : ', model.predict(dog_data).round()) # round함수로 예측률 0 혹은 1로 반환
print('cat data : ', model.predict(cat_data).round())