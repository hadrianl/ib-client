FROM python:3.7.7-slim-stretch

ENV IBHOST host.docker.internal
ENV IBPORT 7496

EXPOSE 6789:6789

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple

COPY . .

CMD python ./main.py ${IBHOST} ${IBPORT}