FROM node:latest as builder
WORKDIR /app
COPY package*.json ./
RUN npm --registry https://registry.npm.taobao.org install
COPY . .
RUN npm run build

From nginx:alpine as production

RUN mkdir /app
COPY --from=builder /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
VOLUME /app/config