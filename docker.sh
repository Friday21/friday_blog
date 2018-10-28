#!/usr/bin/env bash
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
service mysql start
/etc/init.d/nginx start
cd /friday/blog_django
echo yes| python3.6 manage.py collectstatic
gunicorn blog_django.wsgi:application --bind 0.0.0.0:8000 --workers 4