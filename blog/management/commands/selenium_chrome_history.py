# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime, timedelta

import re
import pickle
from django.core.management.base import BaseCommand
from pytz import timezone
from django.utils.timezone import utc
from django.conf import settings

TIME_ZONE = settings.TIME_ZONE

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

from browser_record.models import Domain, ChromeRecord

from tools.time_process import trans_local_to_utc

chromedriver_path = '/usr/bin/chromedriver'
# chromedriver_path = '/a1/static/chromedriver'  # local mac

chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = '/usr/bin/chromium-browser'
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
# proxy = '127.0.0.1:1080'
# chrome_options.add_argument('--proxy-server=socks5://%s' % proxy)

history_url = 'https://myactivity.google.com/item?utm_source=chrome_h'
username = ''
password = ''


class Command(BaseCommand):
    def handle(self, *args, **options):
        last_record = ChromeRecord.objects.first()
        global last_record_time
        last_record_time = last_record.visit_time if last_record else (datetime.now() - timedelta(days=1)).replace(tzinfo=utc)
        browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
        if not open_history(browser):
            open_google_auth(browser)
        time.sleep(10)
        search_history(browser)
        cookies = browser.get_cookies()
        pickle.dump(cookies, open("cookies.pkl", "wb"))


def open_history(browser):
    if not os.path.exists('cookies.pkl'):
        print('no cookie file found')
        return False
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print('open browser')
    browser.get('http://myactivity.google.com')
    print('setting cookie...')
    for cookie in cookies:
        browser.add_cookie(cookie)
    print('open history')
    try:
        browser.set_page_load_timeout(5*60)
        browser.get(history_url)
    except TimeoutException:
        print('time out')
        pass

    try:
        browser.find_element_by_id('gb')
    except NoSuchElementException:
        return False
    print('open history from cookie success')
    return True


def open_google_auth(browser):
    print('google auth')
    url = 'https://accounts.google.com/signin/v2/identifier?hl=zh-CN&passive=true&' \
          'continue=https%3A%2F%2Fmyactivity.google.com%2Fitem%3Futm_source%3Dchrome_h&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    print('start')
    print('open browser')
    browser.set_window_size(1200, 900)
    browser.set_page_load_timeout(5 * 60)
    browser.get(url)
    print('load url')
    time.sleep(10)
    # 找到登录框
    try:
        browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys(username, Keys.ENTER)
    except NoSuchElementException:
        browser.find_element_by_xpath('//*[@id="Email"]').send_keys(username, Keys.ENTER)
    # browser.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()
    time.sleep(10)
    browser.find_element_by_id('Passwd').send_keys(password, Keys.ENTER)
    # browser.find_element_by_xpath('//*[@id="passwordNext"]/content/span').click()
    print('auth success')


def search_history(browser):
    print('finding browser history...')
    h2 = browser.find_elements_by_css_selector('h2.t08.fp-date-block-date')
    scroll_try = 1
    while len(h2) < 2 and scroll_try < 100:
        time.sleep(1)
        scroll_try += 1
        browser.execute_script("""
        var scroll_btn = document.getElementById("main-content");
        scroll_btn.scroll(0, {});""".format(2000*scroll_try))
        print('scroll {}'.format(scroll_try-1))
        h2 = browser.find_elements_by_css_selector('h2.t08.fp-date-block-date')
    try:
        elements = browser.find_elements_by_css_selector('div.fp-display-block-text-holder.layout-align-space-between-stretch.layout-column.flex')
    except TimeoutException:
        print('time out')
        elements = browser.find_elements_by_css_selector('div.fp-display-block-text-holder.layout-align-space-between-stretch.layout-column.flex')
    print(len(elements))
    if len(h2) < 2:
        y_height = float('Inf')
    else:
        y_height = h2[1].location['y']
    analysis_elements(elements, y_height)


def analysis_elements(elements, yesterday_height):
    for element in elements:
        print(element.location, yesterday_height)
        if element.location['y'] >= yesterday_height:
            print('early than yesterday, break')
            break
        content = element.find_element_by_css_selector('h4.fp-display-block-title.t08').get_attribute('innerHTML')
        timer = element.find_element_by_css_selector(
            'div.fp-display-block-details.t12.g6.layout-align-start-center.layout-row').get_attribute('innerHTML')
        try:
            url = re.findall(' href="(.*?)">', content)[0]
            if 'url?q=' in url:
                url = url.split('url?q=')[-1]
            title = re.findall('">\n(.*?)\n', content)[0].strip()
            visit_time = re.findall('>([0-9]{1,2}:[0-9]{2} [AMPM]{2})', timer)[0]

            hour = int(visit_time.split(':')[0])
            if hour != 12 and visit_time[-2:].strip().lower() == 'pm':
                hour += 12
            if hour == 12 and visit_time[-2:].strip().lower() == 'am':
                hour -= 12
            minute = int(visit_time.split(' ')[0].split(':')[1])
            visit_time = datetime.now().replace(hour=hour, minute=minute)
            if local_to_utc(visit_time) < last_record_time:
                break
            # print(url.decode('utf-8'), title.decode('utf-8'), visit_time)
            save_record(url[:250], title[:50], visit_time)
        except IndexError:
            continue


def save_record(url, title, visit_time):
    domain = re.findall('http[s]{0,1}://(.*?)[/?]{1}', url + '/')
    if '10.' in url or '127.0.0.1' in url:
        return
    if 'fridayhaohao' in url:
        return
    if domain:
        domain = domain[0]
        if 'fridayhaohao.com' in domain:
            return
        if domain.count('.') > 1:
            domain = domain[domain.index('.') + 1:]
        domain = Domain.objects.get_or_create(domain=domain)[0]
        domain.visit_count += 1
        domain.last_visited_time = visit_time
        domain.save()
    if visit_time > datetime.now():  # 23:55 分执行时会有日期多加一天的情况
        visit_time -= timedelta(days=1)
    last_record = ChromeRecord.objects.filter(url=url, title=title).first()
    if last_record and trans_local_to_utc(visit_time) - timedelta(minutes=10) < last_record.visit_time < trans_local_to_utc(visit_time) + timedelta(minutes=10):  # 处理重复
        return
    chrome_record = ChromeRecord.objects.get_or_create(
        visit_time=visit_time,
        url=url,
        title=title)[0]
    if domain:
        chrome_record.domain = domain
        chrome_record.save()
    print('save one')


def scroll(browser, y):
    browser.execute_script("""    
                (function () {    
                    var y = %s;    
                    window.scroll(0, y);    
                })();    
            """ % y)


def local_to_utc(local_time):
    """把当地时间转换成utc时间"""
    local = timezone(TIME_ZONE)
    return local.localize(local_time, is_dst=None).astimezone(utc)