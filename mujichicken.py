# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import bs4
import random
import chromedriver_binary
import streamlit as st
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#現在時刻を出力する関数
def now_time():
   dt_now = datetime.datetime.now()
   return dt_now.strftime('%m/%d %H:%M')+' '

def mujichicken_insta(username, password, tagName, likedMax):

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--proxy-server="direct://"')
    options.add_argument('--proxy-bypass-list=*')
    options.add_argument('--start-maximized')

#ブラウザに接続
    DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

#インスタのURLにアクセス
    driver.get("https://www.instagram.com/accounts/login/")
    driver.implicitly_wait(10)
    time.sleep(1)

#メアドと、パスワードを入力
    driver.find_element_by_name('username').send_keys(username)
    time.sleep(2)
    driver.find_element_by_name('password').send_keys(password)
    time.sleep(2)

#ログインボタンを押す
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(3)
    st.write(now_time()+'instagramにログイン')
    time.sleep(1)

#タグ検索
    instaurl = 'https://www.instagram.com/explore/tags/'
    driver.get(instaurl + tagName)

    time.sleep(3)
    st.write(now_time()+'tagで検索中')
    time.sleep(1)

#最新の投稿に画面をスクロール
    target = driver.find_elements_by_class_name('_9AhH0')[10]
    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()
    st.write(now_time()+'最新の投稿まで画面移動')
    time.sleep(3)

#すでにいいねしたかをチェック
    def check_Like():
        html = driver.page_source.encode('utf-8')
        soup = bs4.BeautifulSoup(html, "lxml")
        a = soup.select('span.fr66n')
        return  not '取り消す' in str(a[0])

#最初の投稿にいいねする
    try:
        driver.find_elements_by_class_name('_9AhH0')[9].click()
        time.sleep(random.randint(3, 5))
        st.write(now_time()+'投稿をクリック')
        time.sleep(4)

        if check_Like():
            driver.find_element_by_class_name('fr66n').click()
            st.write(now_time()+'投稿をいいね(1回目)')
            time.sleep(random.randint(3, 5))
        else:
            st.write(now_time()+'いいね済み')

    except WebDriverException:
        st.write(now_time()+'エラーが発生')

#次へボタンを押して、いいねを繰り返す
    for i in range(likedMax-1):
        try:
            driver.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
            st.write(now_time()+'次の投稿へ移動')
            time.sleep(random.randint(3, 5))

        except WebDriverException:
            st.write(now_time()+'{}つ目の位置でエラーが発生'.format(i+2))
            time.sleep(random.randint(4, 10))

        try:
            if check_Like():
                driver.find_element_by_class_name('fr66n').click()
                st.write(now_time()+'投稿をいいね({}回目)'.format(i+2))
                time.sleep(random.randint(3, 5))
            else:
                st.write(now_time()+'いいね済み')
       
        except WebDriverException:
            st.write(now_time()+'{}つ目の位置でエラーが発生'.format(i+3))

## 処理終了
    st.write(now_time()+'終了させてもろて')
    driver.close()
    driver.quit()
