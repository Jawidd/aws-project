FROM node:18-alpine

ENV PORT=3000

COPY . /frontend-react-js

WORKDIR /frontend-react-js

RUN npm install 

EXPOSE ${PORT}


CMD ["npm", "start", "--", "--port", "3000"]



#docker build -t frontend-react-js .\frontend-react-js
    # docker run --rm -p 3000:3000 -it  -e frontend-react-js
    #docker run --rm -p 3000:3000 -it frontend-react-js
