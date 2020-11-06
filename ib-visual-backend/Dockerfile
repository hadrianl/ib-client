FROM python:3.7.7-alpine

ENV IBHOST host.docker.internal
ENV IBPORT 7496

EXPOSE 6789:6789

WORKDIR /usr/src/app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --no-cache wget build-base && \
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -zxvf ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && \ 
    make && make install && \ 
    cd .. && rm -rf ta-lib-0.4.0-src.tar.gz ta-lib/ && \
    pip install --no-cache-dir TA-Lib numpy -i https://pypi.douban.com/simple && \
    apk del wget build-base

# set time zone
RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    date -R && \
    apk del tzdata

COPY . .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple 

# CMD python ./backend.py 