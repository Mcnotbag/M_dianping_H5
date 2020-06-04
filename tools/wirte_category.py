#coding=utf-8
import os
import random
from time import sleep

import psycopg2
import requests
from lxml import etree
# with open('../ch10_list.html','r',encoding='utf-8') as f:
#     text = f.read()
# conn = psycopg2.connect(database="crawler", user="root", password="9TTjkHY^Y#UeLORZ", host="10.101.0.90", port="8635")
# cur = conn.cursor()
proxy = {'http':'http://122.192.174.187:43781','https':'https://122.192.174.187:43781'}
city_en = 'changsha'
city_zh = '长沙'
headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'Referer': 'http://www.dianping.com/nanjing',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }
url = f'http://www.dianping.com/{city_en}/ch10'
resp = requests.get(url=url,headers=headers)
text = resp.content.decode()
print(text)
def category():
    html = etree.HTML(text)
    urls = html.xpath('//div[@id="classfy"]/a/@href')
    titles_1 = html.xpath('//div[@id="classfy"]/a/span/text()')
    for ind,url in enumerate(urls):
        print(url)
        filename = url.split('/')[-1] + '$' + titles_1[ind] + '.txt'
        filenames = [i for i in os.listdir('../category')]
        if filename in filenames:
            print(filename, '已经存在')
            continue
        response = requests.get(url,headers=headers,proxies=proxy)
        html = etree.HTML((response.content.decode()))
        category_3_list = html.xpath('//div[@id="classfy-sub"]/a')
        for category_3 in category_3_list[1:]:
            title = category_3.xpath('./span/text()')[0]
            cate_id = category_3.xpath('./@href')[0].split('/')[-1]
            with open('../category/'+filename,'a',encoding='utf-8') as f:
                f.write(cate_id + '$' + title + '\n')
                print(cate_id + '$' + title + '\n')
        if filename not in [i for i in os.listdir('../category')]:
            with open('../category/'+filename,'w',encoding='utf-8') as f:
                f.write('')
        sleep(random.uniform(2,4))

def region():
    path = f'../region/{city_zh}/'
    html = etree.HTML(text)
    urls = html.xpath('//div[@id="region-nav"]/a/@href')
    titles_1 = html.xpath('//div[@id="region-nav"]/a/span/text()')
    for ind,url in enumerate(urls):
        print(url)
        filename = url.split('/')[-1] + '$' + titles_1[ind] + '.txt'
        filenames = [i for i in os.listdir(path)]
        if filename in filenames:
            print(filename, '已经存在')
            continue
        response = requests.get(url, headers=headers)
        html = etree.HTML((response.content.decode()))
        category_3_list = html.xpath('//div[@id="region-nav-sub"]/a')
        for category_3 in category_3_list[1:]:
            title = category_3.xpath('./span/text()')[0]
            cate_id = 'r' + category_3.xpath('./@data-cat-id')[0]
            with open(path + filename, 'a', encoding='utf-8') as f:
                f.write(cate_id + '$' + title + '\n')
                print(cate_id + '$' + title + '\n')
        if filename not in [i for i in os.listdir(path)]:
            with open(path + filename, 'w', encoding='utf-8') as f:
                f.write('')
        sleep(random.uniform(2, 4))

def get_all_city():
    city_url = 'http://www.dianping.com/citylist'
    resp = requests.get(city_url,headers=headers)
    html = etree.HTML(resp.content.decode())
    city_list = html.xpath("//div[@class='main-citylist']/ul/li/div/div[@class='findHeight']/a")
    for city in city_list:
        city_name = ''.join(city.xpath("./text()"))
        city_url = 'http:'+''.join(city.xpath("./@href"))
        print(city_name,city_url)
        sql = """
        insert into dianping_beauty.dianping_city(name_zh,url) values ('%s','%s')
        """ % (city_name,city_url)
        # cur.cur.execute(sql)
    # conn.commit()
if __name__ == '__main__':
    region()