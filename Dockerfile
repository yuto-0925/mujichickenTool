FROM python:latest

# OSに必要なアプリケーションをインストール
RUN apt-get update && apt-get install -y \
	vim 

# 日本時間に変更
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# pipをアップグレードし、seleniumをインストール
RUN pip install --upgrade pip && pip install \
	numpy \
	pandas \
	streamlit \
	selenium \
	lxml \
	bs4

WORKDIR /work