from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.weather.com.cn/weather/101270101.shtml") \
    .read().decode("utf-8")
print(html)
print("======================================================================================")
soup = BeautifulSoup(html, features="lxml")
all_ul = soup.find_all('ul', attrs={"class": "t clearfix"})
all_li = all_ul[0].find_all("li")
for i in all_li:
    # print(i)
    h1 = i.find("h1").get_text()
    p1 = i.find("p", attrs={"class": "wea"}).get_text()
    p2 = i.find("p", attrs={"class": "tem"})
    tem = p2.find("span").get_text() + "~" + p2.find("i").get_text()
    win = i.find("p", attrs={"class": "win"}).find("i").get_text()

    print(h1)
    print(p1)
    print(tem)
    print(win)
    print("================")
