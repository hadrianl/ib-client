FROM node:latest as builder
WORKDIR /app
COPY package*.json ./
RUN npm --registry https://registry.npm.taobao.org install
COPY . .
RUN npm run build

FROM nginx:alpine as production

ENV APIURL 192.168.2.237:5000

RUN mkdir /app
COPY --from=builder /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
RUN sed -i '22s/${APIURL}/'$APIURL'/' /etc/nginx/nginx.conf
VOLUME /app/config