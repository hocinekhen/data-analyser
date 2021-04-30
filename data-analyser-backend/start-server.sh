#!/usr/bin/env bash
# start-server.sh
#(cd backendProject;python manage.py makemigrations;python manage.py migrate)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    ( 
    python manage.py makemigrations;
    python manage.py migrate; 
    python manage.py createsuperuser --no-input;
    chown -R www-data:www-data db.sqlite3;
    chown -R www-data:www-data jobs.sqlite;)
fi
( envsubst \$listen_port < /opt/app/nginx_template.default  > /etc/nginx/sites-available/default;
    gunicorn data_analyser_project.wsgi:application --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
