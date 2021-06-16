from PIL import Image
import glob
import numpy as np
from sklearn.model_selection import train_test_split

img_dir = '../datasets/train/'
categories = ['cat', 'dog']

# 이미지 크기를 64 X 64 사이즈로 변환
image_w = 64 # 이미지 폭
image_h = 64 # 이미지 높이

# 픽셀 지정
pixel = image_h * image_w * 3 # RGB 3가지 컬러
X = []
Y = []

files = None

# 카테고리별 반복 2회
for idx, category in enumerate(categories): # enumerate로 꺼내오기
    files = glob.glob(img_dir + category + '*.jpg') # 만능문자 *를 이용하여 jpg로 끝나는 모든 파일 가져오기
    for i, f in enumerate(files): # 파일경로를 인덱싱, 경로를 f로 받음
        try:
            # 이미지 파일 열고 RGB로 컨버트하고 리사이징
            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((image_w, image_h)) # 값을 부여할 때, 튜플 형식으로 주기
            data = np.asarray(img) # npasarray함수로 nparrary화
            X.append(data)
            Y.append(idx) # Y에 인덱스 넣기 (cat은 0). categories의 cat과 dog 인덱스를 반환. 즉, Y값이 라벨
            # 300번에 한 번씩 경과 상황 출력하기
            if i % 300 == 0:
                print(category, ':', f)
        # 예외처리
        except:
            print(category, i, '번째에서 에러')

# ndarray로 변환함
X = np.array(X)
Y = np.array(Y)

# 스케일링
X = X / 255

print(X[0])
print(Y[0:5])

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size = 0.1)

xy = (X_train, X_test, Y_train, Y_test)

# 데이터 저장
np.save('../datasets/binary_image_data.npy', xy) # np.save로 저장하면 데이터 그대로 저장하기 때문에 불러올 때도 편리