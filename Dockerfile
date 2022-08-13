FROM ubuntu:22.04

ENV TZ=Asia/Tokyo 
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y build-essential libgomp1 pulseaudio sox git \
  git-lfs julius libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl  \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
  libffi-dev liblzma-dev cmake && \
  apt-get clean

ARG DICTATION_KIT_HASH="1ceb4dec245ef482918ca33c55c71d383dce145e"
RUN git clone https://github.com/julius-speech/dictation-kit.git /opt/dictation-kit && \
  cd /opt/dictation-kit && \
  git checkout ${DICTATION_KIT_HASH} && \
  git lfs fetch origin --recent -I "model/phone_m/jnas-mono-16mix-gid*" && \
  git lfs checkout origin "model/phone_m/jnas-mono-16mix-gid*"

ENV PATH /root/.pyenv/bin:$PATH
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
  pyenv install 3.8.13 && \
  pyenv global 3.8.13 && \
  echo 'eval "$(pyenv init --path)"' >> /root/.bashrc && \
  ( cd /tmp && curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py )


WORKDIR /usr/src/app
COPY . /usr/src/app
RUN . /root/.bashrc && pip3 install pyopenjtalk

ENV PYTHONPATH /usr/src/app/ext/julius4seg
ENV HMM_MODEL /opt/dictation-kit/model/phone_m/jnas-mono-16mix-gid.binhmm