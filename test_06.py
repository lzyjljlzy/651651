from bs4 import BeautifulSoup
import bs4, csv, numpy
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
browser.get('http://www.jd.com')
wait = WebDriverWait(browser, 5)
input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label=搜索]')))
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label=搜索]')))
input.clear()
input.send_keys('python')
submit.click()
time.sleep(2)
js = "document.documentElement.scrollTop=10000"
browser.execute_script(js)
time.sleep(2)

books = []


def get_info(html):
    soup = BeautifulSoup(html, 'lxml')
    tag_img = soup.select('#J_goodsList > ul > li > div > div.p-img')
    tag_price = soup.select('#J_goodsList > ul > li > div > div.p-price')
    tag_name = soup.select('#J_goodsList > ul > li > div > div.p-name > a > em')
    tag_publish = soup.select('#J_goodsList > ul > li > div > div.p-shopnum')
    tag_comment = soup.select('#J_goodsList > ul > li > div > div.p-commit')
    # advertising = soup.select('# J_goodsList > ul > li > div > div.p-market')

    for i in range(0, len(tag_img)):
        temp = []
        temp.append(tag_name[i].text)
        temp.append(tag_price[i].text.strip().replace('\n', ''))
        temp.append(tag_img[i].a.img)
        temp.append(tag_comment[i].text.replace('\n', ''))
        temp.append(tag_publish[i].text.replace('\n', ''))
        books.append(temp)


def next_page():
    try:
        wait = WebDriverWait(browser, 10)
        nextpage = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pn-next > em')))
        nextpage.click()
        time.sleep(2)
        js = "document.documentElement.scrollTop=10000"
        browser.execute_script(js)
    except TimeoutException:
        next_page()


def save_data(data):
    with open('京东-python 图书信息.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['名称', '价格', '封面', '评论数', '出版社'])
        for a in data:
            print(a)
            writer.writerow(a)


for i in range(0, 168):
    html = browser.page_source
    get_info(html)
    next_page()
    time.sleep(5)
save_data(books)
browser.quit()
