import os
import bs4
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import lxml

def getHTML(url):
    try:
        r = requests.get(url,timeout = 10,headers = hd)
        r.raise_for_status()       #容错机制，若请求访问失败则返回的不是200，则返回字符串空
        r.encoding = r.apparent_encoding     #设置编码方式，用解析返回网页源码得出的编码方式代替  UTF-8
        return r.text
    except:
        return ''

hd = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
url = "https://www.mh1234.com/comic/15632.html"

text = getHTML(url)
soup = BeautifulSoup(text,'lxml')

b = soup.select('div#play_0 > ul > li > a')

dict = {}
#控制页数
#101实测是从99话开始,末尾是len(b)
#现在解决下速度的问题还有selenium的弹窗问题
for _ in range(79,102):
    dict[b[_].text] = b[_]["href"]



url_left = "https://www.mh1234.com"


# 加载启动项
option = webdriver.ChromeOptions()
option.add_argument('headless')


driver = webdriver.Chrome(options = option)
driver.set_page_load_timeout(30)
driver.set_script_timeout(30) 

for name_folder in dict:
    url_right = dict[name_folder]
    if not os.path.exists(name_folder):     #os模块判断并创建
        os.mkdir(name_folder)
    url_page = url_left + url_right
    try:
        driver.get(url_page)
        sourcePage = driver.page_source
        soup = BeautifulSoup(sourcePage, "lxml")
        index = soup.select('div.picNav > select > option')
        max_page = index[-1]['value']
        max_page = int(max_page)

    except:
        print("响应太慢")
        driver.execute_script("window.stop()")
        pass
    for i in range(max_page):
        url_pic = url_page + '?p=' +str(i+1)

        try:
            driver.get(url_pic)
            sourcePage = driver.page_source
            soup = BeautifulSoup(sourcePage, "lxml")
            #筛选出图片地址标签
            a = soup.select('div#images > img')[0]
            #获取图片的地址和图片的名称
            url_p = a.attrs['src']
            name_p = a.attrs['data-index'] + '.jpg'
            #get 获取图片内容
            img_data = requests.get(url=url_p)
            #选择该话的路径
            img_path = name_folder
            #保存文件
            with open(img_path+'/'+name_p,'wb') as fp:
                fp.write(img_data.content)
            print(i+1,'/',max_page, name_folder)
        except:
            print("响应太慢")
            driver.execute_script("window.stop()")

