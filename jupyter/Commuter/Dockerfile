FROM  node:8.16.0-alpine
RUN apk add python
RUN apk add pkgconfig
RUN apk add make
RUN apk add g++
RUN apk add pixman
RUN mkdir -p /home/node && chown -R node:node /home/node
WORKDIR /home/node/app
USER node
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
RUN npm install @nteract/commuter -g