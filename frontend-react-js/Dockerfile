FROM node:18-alpine

WORKDIR /frontend-react-js

COPY package*.json ./
RUN npm ci

COPY . .

ENV PORT=3000
EXPOSE 3000

CMD ["npm", "start"]


# Frontend  
#docker build -t frontend-react-js ./frontend-react-js
#docker run --rm -p 3000:3000 --env-file .env frontend-react-js

