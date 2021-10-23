import requests
import time
from bs4 import BeautifulSoup
import re
import os

'''
1、爬取大页面数据，并获取小页面的网址
2、获取小页面网址中的数据，并找出里面图片的地址
3、创建关于小页面的文件夹
4、保存图片
'''

def one(url,headers):
    responses = requests.get(url, headers=headers)  # 获取最开始的大页面的数据
    html = responses.text  # 将最开始大页面的数据以txt形式暂存
    targets = BeautifulSoup(html, "html.parser").find_all("h2", class_="post-box-title")  # 解析最开始的大页面，并找到每一个子网页所在的标签
    return targets

def two(url,headers):
    responses = requests.get(url, headers=headers)  # 获取小页面的数据
    html = responses.text  # 小页面的数据以txt形式暂存
    find = BeautifulSoup(html, 'html.parser').find("div", class_="entry").find_all("img")  # 解析小页面页页面的数据，并找<div>的父标签，接着找到<img>子标签

def three(html,dir_path):
    dir_name = dir_path + str(re.findall('<span itemprop="name">(.*?)</span>', html)[0])[0:14]  # 目录地址+文件夹名称=目录下的文件名称
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(dir_name + '创建完成')

def four(url,headers,dir_name):
    time.sleep(1)
    responses = requests.get(url['src'], headers=headers)
    file_name = str(nu) + '.jpg'  # 定义图片的名字
    with open(dir_name + '/' + file_name, 'wb')as f:  # 'wb'表示以二进制形式保存，dir_name + '/' + file_name表示地址
        f.write(responses.content)  # content:内容
        print("第%d张下载成功" % num)

if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    nu = 0
    num = 0
    dir_ = str(input("请问你想将图片放入哪个硬盘（输入盘符）："))
    dir = str(input("请问你想为放入图片的文件夹创建什么名字："))
    number = int(input("请问你想总共下载多少页的呢："))
    domain = 'http://acg17.com/tag/pixiv/page/'
    page = str(int(input("请问你想从第几页开始下载呢：")))
    total_url = domain + page + '/'































