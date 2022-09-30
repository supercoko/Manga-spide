import os
import bs4
import re
import time
import requests
from bs4 import BeautifulSoup

def getHTMLText(url, headers):
    """向目标服务器发起请求并返回响应"""
    try:
        r = requests.get(url=url, headers=headers)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    except:
        return "失败"

def CreateFolder():
    """创建存储数据文件夹"""
    flag = True
    while flag == 1:
        file = input("请输入保存数据文件夹的名称：")
        if not os.path.exists(file):
            os.mkdir(file)
            flag = False
        else:
            print('该文件已存在，请重新输入')
            flag = True

    # os.path.abspath(file)  获取文件夹的绝对路径
    path = os.path.abspath(file) + "\\"
    return path

def fillUnivList(ulist, soup):
    """获取每一张图片的原图页面"""
    # [0]使得获得的ul是 <class 'bs4.BeautifulSoup'> 类型
    div = soup.find_all('div', 'list')[0]
    for a in div('a'):
        if isinstance(a, bs4.element.Tag):
            hr = a.attrs['href']
            href = re.findall(r'/desk/[1-9]\d{4}.htm', hr)
            if bool(href) == True:
                ulist.append(href[0])

    return ulist

def DownloadPicture(left_url,list,path):
    for right in list:
        url = left_url + right
        r = requests.get(url=url, timeout=26)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,"html.parser")
        tag = soup.find_all("p")
        # 获取img标签的alt属性，给保存图片命名
        name = tag[0].a.img.attrs['alt']
        img_name = name + ".jpg"
        # 获取图片的信息
        img_src = tag[0].a.img.attrs['src']
        try:
            img_data = requests.get(url=img_src)
        except:
            continue

        img_path = path + img_name
        with open(img_path,'wb') as fp:
            fp.write(img_data.content)
        print(img_name, "   ******下载完成！")

def PageNumurl(urls):
    num = int(input("请输入爬取所到的页码数："))
    for i in range(2,num+1):
        u = "http://www.netbian.com/index_" + str(i) + ".htm"
        urls.append(u)

    return urls


if __name__ == "__main__":
    url = "https://www.mh1234.com/comic/15632.htm"
    uinfo = []
    left_url = "http://www.netbian.com"
    urls = ["http://www.netbian.com/index.htm"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    start = time.time()
    # 1.创建保存数据的文件夹
    path = CreateFolder()
    # 2. 确定要爬取的页面数并返回每一页的链接
    PageNumurl(urls)
    n = int(input("访问的起始页面："))
    for i in urls[n-1:]:
        # 3.获取每一个页面的首页数据文本
        soup = getHTMLText(i, headers)
        # 4.访问原图所在页链接并返回图片的链接
        page_list = fillUnivList(uinfo, soup)
        # 5.下载原图
        DownloadPicture(left_url, page_list, path)

    print("全部下载完成！", "共" + str(len(os.listdir(path))) + "张图片")
    end = time.time()
    print("共耗时" + str(end-start) + "秒")
