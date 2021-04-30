# Dockerfile

# FROM directive instructing base image to build upon
FROM python:3.7-buster
# add the Nginx installation commands and COPY the configuration file inside the container
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
RUN apt-get install -y gettext-base
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/data_analyser_project
RUN mkdir -p ~/opt/app/media

COPY requirements.txt start-server.sh /opt/app/
COPY manage.py /opt/app/
COPY nginx_template.default /opt/app/
COPY data_analyser_project /opt/app/data_analyser_project/
COPY data_analyser_app /opt/app/data_analyser_app/
COPY media /opt/app/media/


WORKDIR /opt/app
ENV listen_port 8000
RUN pip3 install -r requirements.txt
#run unit tests
RUN python3 manage.py test 
RUN pip3 install -r requirements.txt
RUN chown -R www-data:www-data /opt/app
RUN chmod +x /opt/app/start-server.sh
# start server
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]
