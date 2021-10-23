import time
from bs4 import BeautifulSoup
import os
import threading
import re
import requests

def get_all_urls(url):
    responses = requests.get(url,headers = headers)
    html = responses.text
    soup_1 = BeautifulSoup(html,"lxml").find_all("article",class_ = "item-list")
    soup_2 = re.findall("<a href=\"(.*html)\">.*</a>",str(soup_1))
    return soup_2 # 得到全部画集url列表

def get_images_urls(url):
    responses = requests.get(url, headers=headers)
    html = responses.text
    soup_1 = BeautifulSoup(html, "lxml").find("div", class_="entry").find_all("img")
    soup_2 = re.findall("<img alt=\".*?\" src=\"(.*?)\" title=\".*?\"",str(soup_1))
    return soup_2 # 得到全部图片url列表，在这需要将全部的url，分成和线程相等的份数，每一份为单独的一个列表

def download_img(image_url,dir_path,num):
    file_name = str(num) + ".jpg"
    file_path = dir_path + "/" + file_name
    responses = requests.get(image_url,headers = headers)
    with open(file_path,"ab+") as f:
        f.write(responses.content)
    f.close()

def average(image_urls,list_num):
    bl = []
    for i in range(0,len(image_urls),list_num):
        sl = image_urls[i : i + list_num]
        bl.append(sl)
    return bl

def begin_download(c):
    global num
    for i in average(image_urls,list_num)[c]:
        lock.acquire()
        download_img(i,dir_path,num)
        print("第{}张下载完成".format(num))
        lock.release()
        num += 1
        time.sleep(1)

if __name__ == '__main__':
    start = time.time()
    dir_ = str(input("请问你想将图片放入哪个硬盘（输入盘符）："))
    dir = str(input("请问你想为放入图片的文件夹创建什么名字："))
    dir_path = dir_ + ':' + '/' + dir
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    print("开始检测url......")
    num = 1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    url = "http://acg17.com/category/meitu/pixiv-wallpaper/"
    lock = threading.Lock()
    image_urls = [] #创建一个全部图片的url列表
    threads = [] #创建一个线程列表
    count = 15 # 确定20条线程
    list_num = 0 #每条线程所要下载的图片数量
    for urls in get_all_urls(url):
        for images_urls in get_images_urls(urls):
            image_urls.append(images_urls)

    if len(image_urls) % count != 0:
        list_num = len(image_urls) // count + 1
    else:
        list_num = len(image_urls) / count

    for i in range(count):
        thread = threading.Thread(target=begin_download,args=(i,),name="线程{}".format(i))
        threads.append(thread)

    for i in threads:
        i.start()
    for i in threads:
        i.join()
    end = time.time()
    print("下载完成，总共下载{}张图".format(num-1))
    print("消耗时间为：{:.4f}秒".format(end - start))