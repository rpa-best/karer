FROM node:lts-alpine

# make the 'app' folder the current working directory
WORKDIR /app


# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .
RUN npm cache clear -f
RUN npm ci

ENV HOST=0.0.0.0
ENV PORT=4000
ENV NITRO_HOST=0.0.0.0
ENV NITRO_PORT=4000

EXPOSE 4000

RUN npm run build
CMD ["npm", "run", "preview"]