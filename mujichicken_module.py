import streamlit as st
import mujichicken

st.title('Mujichicken Auto-Instagram')

username=st.text_input('Username')
password=st.text_input("Password", type="password")
tagName=st.text_input('ハッシュタグ(#不必要)')
likedMax=st.number_input('自動いいね数', 10, 10000)

answer = st.button('スタート')

if answer == True:
     mujichicken.mujichicken_insta(username, password, tagName, likedMax)
     st.write('またやりたかったらスタート押してね')
else:
     st.write('')
