FROM node:20.10.0

WORKDIR /usr/src/healthchatbot

# COPY package*.json yarn.lock ./
COPY . .
# RUN yarn install
RUN npm install

EXPOSE 3000

CMD  ["npm", "run", "dev"]
