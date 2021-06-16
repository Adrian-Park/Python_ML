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

title_list = []

for k in range(101, 201):
    url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=102#&date=%2000:00:00&page={}'.format(k)
    df_title = pd.DataFrame()
    for j in range(1, 5):
        for i in range(1, 6):
            try:
                driver.get(url)
                title = driver.find_element_by_xpath('//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(j, i)).text
                title = (re.compile('[^가-힣|a-z|A-Z]').sub(' ', title))
                title_list.append(title)

            except NoSuchElementException:
                print('NoSuchElementException')
            # except StaleElementReferenceException:
            #     print('StaleElementReferenceException')
            except:
                print('other error')

df_section_title = pd.DataFrame(title_list)
df_section_title['category'] = 'Social'
df_title = pd.concat([df_title, df_section_title], axis=0, ignore_index=True)

# 드라이버 종료
driver.close()

df_title.to_csv('./crawling_data/2.csv')