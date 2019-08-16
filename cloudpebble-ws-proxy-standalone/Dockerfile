FROM node:8-alpine

COPY . /code
WORKDIR /code

RUN npm install 
RUN npm install dotenv sanity ws koa koa-route co bunyan request
CMD ["node start.js"]
