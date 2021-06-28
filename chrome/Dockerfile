FROM selenium/node-chrome-debug
LABEL authors=SeleniumHQ
USER root
#=================
# Locale settings
#=================
ENV LANGUAGE ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
RUN locale-gen ja_JP.UTF-8 \
  && dpkg-reconfigure --frontend noninteractive locales \
  && apt-get update -qqy \
  && apt-get -qqy --no-install-recommends install \
    language-pack-ja \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

USER seluser
EXPOSE 5900 