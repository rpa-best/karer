FROM node:lts-slim

COPY package*.json ./

RUN npm install

# make the 'app' folder the current working directory
WORKDIR /app


# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000
