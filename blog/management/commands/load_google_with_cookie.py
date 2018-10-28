import pickle

from selenium import webdriver
from selenium.common.exceptions import TimeoutException


chromedriver_path = '/home/friday/myproject/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
proxy = '127.0.0.1:1080'
chrome_options.add_argument('--proxy-server=socks5://%s' % proxy)
history_url = 'https://myactivity.google.com/item?utm_source=chrome_h'

browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

cookies = pickle.load(open("cookies_firefox.pkl", "rb"))
print('open browser')
browser.get('http://myactivity.google.com')
print('setting cookie...')
for cookie in cookies:
    cookie['domain'] = 'myactivity.google.com'
    browser.add_cookie(cookie)
print('open history')
try:
    browser.set_page_load_timeout(5*60)
    browser.get(history_url)
except TimeoutException:
    print('time out')