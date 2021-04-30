### STAGE 1: Build ###
FROM node:12.7-alpine as build
WORKDIR /usr/src/app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

### STAGE 2: Run ###
FROM nginx:stable-alpine
COPY default.conf /etc/nginx/conf.d/default.conf
COPY nginx_template.default /etc/nginx/conf.d/nginx_template.default
COPY --from=build /usr/src/app/dist /usr/share/nginx/html
EXPOSE 80
