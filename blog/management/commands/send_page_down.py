import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


history_url = 'https://myactivity.google.com/item?utm_source=chrome_h'

profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks_port', 1080)
profile.set_preference('network.proxy.socks', "127.0.0.1")
profile.update_preferences()

browser = webdriver.Firefox(firefox_profile=profile, executable_path='/home/friday/myproject/geckodriver')


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
# page = browser.find_element_by_tag_name('body')
# page = browser.find_element_by_xpath('//*[@id="main-content"]')
page = browser.find_element_by_id('main-content')
# page.click()

for i in range(1, 101):
    page.send_keys(Keys.PAGE_DOWN)
    print(i)
    time.sleep(1)