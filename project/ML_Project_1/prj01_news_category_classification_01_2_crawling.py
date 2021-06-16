# 모듈 임포트
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import re

# 크롬 드라이버 옵션 설정
# 크롬 드라이버 사용 시 기본 옵션이라고 생각
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage') #
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options) # 웹드라이버로 크롬 브라우저 열기
driver.implicitly_wait(10) # 행동 시 wait 시간 (크롤링하며 적절히 조절)

# 한 페이지 잘 크롤링 해오는지 test
# try:
#     driver.get(url)
#     title = driver.find_element_by_xpath( # xpath로 크롤링
#         '//*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a'
#     ).text # text로 변환
#     title = (re.compile('[^가-힣|a-z|A-Z]').sub(' ',title))
#     print(title)
# except NoSuchElementException:
#     print('NoSuchElementException')

# 카테고리 만듦
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
# 각 카테고리 별 최대 페이지 설정
page_num = [334, 423, 400, 87, 128, 74]
# 빈 DF 생성
df_title = pd.DataFrame()

# 카테고리 바꾸는 for문
for l in range(0, 6):
    df_section_title = pd.DataFrame()  # 빈 데이터프레임 생성
    # 주소 바꾸는 for문
    for k in range(1, 2):
        url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(l,k)
        title_list = []
        # 헤드라인 xpath로 가져오기
        for j in range(1, 5):
            for i in range(1, 6):
                try:
                    driver.get(url)
                    title = driver.find_element_by_xpath(  # xpath로 크롤링 / selector로 사용시 by_css_selector 함수 사용
                        '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(j, i) # 앞 {}이 j, 뒤 {}이 i
                    ).text  # text로 변환후 title 변수에 저장
                    title = (re.compile('[^가-힣|a-z|A-Z]').sub(' ', title))
                    print(title)
                    title_list.append(title) # 20개가 title_list에 append
                except NoSuchElementException: # xpath에 해당되는 기사가 없을 시 예외 처리
                    print('NoSuchElementException')
    df_section_title = pd.DataFrame(title_list, columns=['title'])
    df_section_title['category'] = category[l] # 카테고리 컬럼 추가
    df_title = pd.concat([df_title, df_section_title], axis=0, ignore_index=True)

# 드라이버 종료
driver.close()
df_title.head(30)

df_title.to_csv('./crawling_data/naver_news_titles_20210615.csv')

# //*[@id="section_body"]/ul[1]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[2]/dl/dt[2]/a
# //*[@id="section_body"]/ul[1]/li[3]/dl/dt[2]/a

# xpath는 5개씩 끊긴다. => 처음 5개 ul은 [1] 그 이후 5개는 [2]이다.
# //*[@id="section_body"]/ul[2]/li[1]/dl/dt[2]/a