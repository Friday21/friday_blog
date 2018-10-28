import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


chromedriver_path = '/home/friday/myproject/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
proxy = '127.0.0.1:1080'
chrome_options.add_argument('--proxy-server=socks5://%s' % proxy)

username = ''
password = ''


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
    try:
        browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys(username)
    except NoSuchElementException:
        browser.find_element_by_xpath('//*[@id="Email"]').send_keys(username)
    browser.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()
    time.sleep(10)
    browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
    browser.find_element_by_xpath('//*[@id="passwordNext"]/content/span').click()
    print('auth success')

if __name__ == '__main__':
    browser = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
    open_google_auth(browser)