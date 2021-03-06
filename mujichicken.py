# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import datetime
import bs4
import random
from selenium.webdriver.common.keys import Keys
import os

import streamlit as st


#現在時刻を出力する関数
def now_time():
   dt_now = datetime.datetime.now()
   return dt_now.strftime('%m/%d %H:%M')+' '

def mujichicken_insta(username, password, tagName, likedMax):

    options = Options()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9515')
    options.add_argument('--disable-setuid-sandbox')
    
#ブラウザに接続
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.implicitly_wait(10)
    time.sleep(5)

#インスタのURLにアクセス
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    st.write(now_time()+'instagramにアクセス')
    driver.implicitly_wait(10)
    driver.delete_all_cookies()

#メアドと、パスワードを入力
    user = driver.find_element_by_xpath('//input[@name="username"]')
    user.send_key(username)
    time.sleep(1)
    passwords = driver.find_element_by_xpath('//input[@name="password"]')
    passwords.send_key(password)
    time.sleep(1)

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
