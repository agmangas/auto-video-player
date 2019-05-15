FROM nginx:1.15
COPY default.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html/