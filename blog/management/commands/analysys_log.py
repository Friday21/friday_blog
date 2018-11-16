# -*- coding: utf-8 -*-

import logging
import re
from datetime import datetime

import requests
import geoip2.database
from django.core.management.base import BaseCommand
from blog.models import AccessLog, Article

logger = logging.getLogger(__name__)
ACCESS_LOG_DIR = '/var/log/nginx'
log_file = ACCESS_LOG_DIR + '/access.log'
geoip_db = '/friday/data/geodb/GeoLite2-City.mmdb'
TIME_FORMAT = '%d/%b/%Y:%H:%M:%S'


class Command(BaseCommand):
    def handle(self, *args, **options):
        reader = geoip2.database.Reader(geoip_db)
        with open(log_file) as f:
            for line in f.readlines():
                try:
                    ip, _, refer, ua, url, status, access_time, fp2, language, resolution, platform = line.split(',####')
                    if ip == '127.0.0.1':
                        continue
                    url = url.replace('GET', '').replace('HTTP/1.1', '').replace('HTTP/1.0', '')
                    if useless_log(url, ua, status):
                        continue
                    access_time = datetime.strptime(access_time.split(' ')[0], TIME_FORMAT)
                    if AccessLog.objects.filter(access_time=access_time, ua=ua, url=url).exists():
                        continue

                    dev = guess_device(ua)
                    browser = guess_browser(user_agent=ua)
                    if not dev and not browser:
                        continue

                    try:
                        response = reader.city(ip)
                        address = '%s %s' % (response.country.name, response.city.name)
                    except Exception as e:
                        print(e)
                        address = ''
                    if fp2 != '-' and AccessLog.objects.filter(fp2=fp2, memo__isnull=False).exclude(memo='').exists():
                        memo = 'fp: ' + AccessLog.objects.filter(fp2=fp2, memo__isnull=False).exclude(memo='').first().memo.replace('New_', '')
                    elif fp2 != '-':
                        memo = 'New_' + str(AccessLog.objects.filter(memo__startswith='New_').count())
                    elif 'article' not in url:
                        continue
                    else:
                        memo = ''

                    if '李东勇' in memo:
                        continue

                    if AccessLog.objects.filter(ip=ip, ip138__isnull=False).exclude(ip138='').exists():
                        ip138 = AccessLog.objects.filter(ip=ip, ip138__isnull=False).exclude(ip138='').first().ip138
                    else:
                        ip138 = get_ip138_address(ip)
                    access_log = AccessLog(ip=ip,
                                           refer=refer,
                                           ua=ua,
                                           url=url,
                                           dev=dev,
                                           address=address,
                                           browser=browser,
                                           memo=memo,
                                           ip138=ip138,
                                           access_time=access_time,
                                           fp2=fp2,
                                           language=language,
                                           resolution=resolution,
                                           platform=platform)
                    access_log.save()
                    update_count(url)
                    print('-----------Done-------------------')
                except Exception as e:
                    print(str(e))
                    raise e
                    logger.error('Error when analysys accesslog, %s' % e)
        reader.close()


def guess_browser(user_agent):
    ua = user_agent.lower()
    browser = ''
    if 'iphone' in ua and 'safari/' in ua:
        browser = 'Safari'
    elif 'mac os' in ua and 'safari/' in ua:
        browser = 'Safari'
    elif 'android' in ua and 'linux' in ua:
        browser = 'Android browser'
    elif 'chromium/' in ua:
        browser = 'Chromium'
    elif 'chrome/' in ua:
        browser = 'Chrome'
    elif 'firefox/' in ua:
        browser = 'Firefox'
    elif 'msie' in ua:
        browser = 'IE'
    return browser


def guess_device(ua):
    dev = ''
    if 'iphone' in ua.lower():
        dev = 'iPhone'
    elif 'ipad' in ua.lower():
        dev = 'iPad'
    elif 'macintosh' in ua.lower() or 'mac os' in ua.lower():
        dev = 'Macintosh'
    elif 'android' in ua.lower():
        dev = 'Android'
    elif 'linux' in ua.lower():
        dev = 'Linux'
    elif 'windows nt' in ua.lower() or 'windowsnt' in ua.lower():
        dev = 'windows'
    return dev


def get_ip138_address(ip):
    url = 'http://api.ip138.com/query/'
    params = {'ip': ip, 'datatype': 'json'}
    headers = {'token': '3cfc3a1af13b49d3ffbda041f16f109d'}
    resp = requests.get(url=url, params=params, headers=headers)
    if resp.status_code != 200:
        return 'ip138错误' + str(resp.status_code)
    return resp.content.decode('utf-8').replace(ip, '')


def useless_log(url, ua, status):
    key_words = ['spider', 'bot', 'alibaba', 'wget', 'phantomjs', 'google favicon', 'python-requests']
    for word in key_words:
        if word in ua.lower():
            return True
    if 'static' in url or status != '200':
        return True
    if ua == '-':
        return True
    if 'xadmin' in url:
        return True
    if 'robot' in url:
        return True
    return False


def update_count(url):
    url = url.strip()
    if re.match('/articles/([0-9]+)/', url):
        article_id = int(re.findall('/articles/([0-9]+)/', url)[0])
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            logger.error('aricle不存在， article_id:{}'.format(article_id))
            return
        article.view_count += 1
        article.save()