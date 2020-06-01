#coding:utf-8
import hashlib
import json
import os
import random
import threading
from datetime import datetime
from pprint import pprint
from time import sleep, time

import psycopg2
import requests
from redis import Redis

from tools.proxy import taiyang_proxy,abuyun
from get_shop_comment import Shop_Comment
from fake_useragent import UserAgent
ua = UserAgent(path='tools/ua.json')
# 线上
conn = psycopg2.connect(database="crawler", user="root", password="9TTjkHY^Y#UeLORZ", host="10.101.0.90", port="8635")
# 本地
# conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="postgres", host="localhost", port="8635")

cur = conn.cursor()
# 本地
# redis_cli = Redis(decode_responses=True)
# 线上
redis_cli = Redis(host='10.101.0.239',password='abc123',decode_responses=True)
redis_name = 'dp_ch10'
# proxy = taiyang_proxy()
# proxy = {'http': 'http://182.84.112.52:4317', 'https': 'https://182.84.112.52:4317'}

def enpytro():
    s = hex(int(65536 * (1 + random.random())))
    return s.replace('0x','')[1:]

def get_hc_v():
    return enpytro() + enpytro() + "-" + enpytro() + "-" + enpytro() + "-" + enpytro() + "-" + enpytro() + enpytro() + enpytro() + '.' + str(int(time()))



class dp_meishi:
    def __init__(self,dp_args):
        self.proxy = taiyang_proxy()
        self.g_id = None
        self.r_id = None
        self.page = 1
        self.args = dp_args
        self.page_count = 1
        self.list_url = 'http://www.dianping.com/search/map/ajax/json'
        self.headers = {
        'Accept': 'application/json, text/javascript',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
        'Host': 'www.dianping.com',
        'Origin': 'http://www.dianping.com',
        'Referer': 'http://www.dianping.com/search/map/category/7/10/g112',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        # 'Cookie': 's_ViewType=10; _lxsdk_cuid=17263a5f11cc8-0a35404038c5e8-f7d1d38-1fa400-17263a5f11c6f',
            'Cookie':"_hc.v={};s_ViewType=10;".format(get_hc_v()),
        'X-Request': 'JSON',
        'X-Requested-With': 'XMLHttpRequest',
        }
        self.data = {
            'cityId': '7',
            'cityEnName': 'shenzhen',
            'promoId': '0',
            'shopType': '10',
            'categoryId': '112',
            'regionId': '0',
            'sortMode': '2',
            'shopSortItem': '0',
            'keyword': '',
            'searchType': '1',
            'branchGroupId': '0',
            'aroundShopId': '0',
            'shippingTypeFilterValue': '0',
            'page': '1',
        }
        payload = 'cityId=7&cityEnName=shenzhen&promoId=0&shopType=10&categoryId=34224&regionId=28441&sortMode=2&shopSortItem=0&keyword=&searchType=1&branchGroupId=0&aroundShopId=0&shippingTypeFilterValue=0&page=1'

    def get_list(self,page,kwargs):
        self.headers['Referer'] = 'http://www.dianping.com/search/map/category/7/10/' + self.g_id
        self.data['categoryId'] = self.g_id.replace('g', '')
        self.data['regionId'] = self.r_id.replace('r','')
        self.data['page'] = str(page)
        print('当前IP：',self.proxy)
        try:
            response = requests.post(self.list_url, headers=self.headers, data=self.data,proxies=self.proxy,verify=False,timeout=8)
        except:
            self.proxy = taiyang_proxy()
            response = requests.post(self.list_url, headers=self.headers, data=self.data,proxies=self.proxy,verify=False)
        # print(response.content.decode())
        if response.status_code == 200:
            json_resp = json.loads(response.content.decode())
            if json_resp['code'] == 200:
                self.page_count = json_resp['pageCount']
                for shop in json_resp['shopRecordBeanList']:
                    kwargs['shopid'] = shop['shopId']
                    kwargs['shopname'] = shop['shopName'].replace("'",'‘')
                    kwargs['shop_score'] = shop['shopPower']
                    kwargs['star_score'] = shop['shopPowerTitle']
                    kwargs['url'] = 'http://www.dianping.com/shop/'+ shop['shopId']
                    kwargs['address_gps_lng'] = shop['geoLng']
                    kwargs['address_gps_lat'] = shop['geoLat']
                    kwargs['address'] = shop['address']
                    kwargs['avg_spend'] = shop['avgPrice']
                    # sleep(random.uniform(0.2,0.5))
                    # print(kwargs['url']+ '/review_all')

                    detail_obj = Shop_Comment(kwargs['url']+ '/review_all',proxy=self.proxy)
                    info_kwargs,comm_kwargs_list = detail_obj.run()
                    kwargs.update(info_kwargs)
                    kwargs = self.clean_kwargs(**kwargs)
                    self.insert_shop_info(**kwargs)
                    self.insert_comment(comm_kwargs_list)
            else:
                print(response.content.decode())
                self.proxy = taiyang_proxy()
                redis_cli.sadd(redis_name,self.args)

    def pre_args_str(self):
        kwargs = {}
        dp_args = self.args
        kwargs['source_data'] = '大众点评'
        kwargs['category_tags_l1_name'] = '美食'
        kwargs['category_tags_l2_name'] = dp_args.split(';')[0].split('$')[1]
        kwargs['category_tags_l3_name'] = dp_args.split(';')[1].split('$')[1]
        self.g_id = dp_args.split(';')[1].split('$')[0]
        kwargs['city'] = '深圳市'
        kwargs['district'] = dp_args.split(';')[2].split('$')[1]
        if len(dp_args.split(';')) == 3:
            kwargs['region'] = ''
            self.r_id = dp_args.split(';')[2].split('$')[0]
        else:
            kwargs['region'] = dp_args.split(';')[3].split('$')[1]
            self.r_id = dp_args.split(';')[3].split('$')[0]
        return kwargs

    def clean_kwargs(self,**kwargs):
        # 生成id
        hash_str = kwargs['source_data'] + '$' + kwargs['shopname'] + '$' + kwargs['address'] + '$' + str(kwargs['address_gps_lng']) + '$' + str(kwargs['address_gps_lat'])
        kwargs['id'] = hashlib.md5(hash_str.encode('utf-8')).hexdigest()
        # 评论数
        try:
            kwargs['comment_cnt'] = kwargs['comment_cnt'].replace('条评论','')
        except:
            kwargs['comment_cnt'] = '0'
        # 环境评分
        try:
            kwargs['env_score'] = kwargs['env_score'].replace('环境：','')
        except:
            kwargs['env_score'] = 0
        if kwargs['env_score'] == '':
            kwargs['env_score'] = 0
        # 口味评分
        try:
            kwargs['pro_score'] = kwargs['pro_score'].replace('口味：','')
        except:
            kwargs['pro_score'] = 0
        if kwargs['pro_score'] == '':
            kwargs['pro_score'] = 0
        # 服务评分
        try:
            kwargs['ser_score'] = kwargs['ser_score'].replace('服务：','')
        except:
            kwargs['ser_score'] = 0
        if kwargs['ser_score'] == "":
            kwargs['ser_score'] = 0
        # 人均消费
        if kwargs['avg_spend'] == -1:
            kwargs['avg_spend'] = 0
        # 创建时间
        kwargs['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 评论标签
        if 'comment_tags' not in kwargs.keys():
            kwargs['comment_tags'] = ''

        return kwargs

    def insert_comment(self,comment_list):
        for comment in comment_list:
            sql = """
            insert into dianping_comment values ('%(id)s','%(shopid)s','%(shopname)s','%(comment)s','%(url)s','%(user_name)s','%(user_level)s','%(user_vip)s','%(pro_score)s',
            '%(env_score)s','%(ser_score)s','%(com_date)s','%(create_time)s','%(shop_score)s')
            """ % comment
            try:
                cur.execute(sql)
            except:
                # print('评论已存在',comment['id'],'店名:',comment['shopname'])
                pass
        conn.commit()
        print('评论插入成功：', comment_list[0]['shopname'])

    def insert_shop_info(self,**kwargs):
        sql = """
            insert into dianping_shop values (
            '%(source_data)s','%(id)s','%(shopname)s','%(shopid)s','%(url)s','%(address)s','%(city)s','%(district)s','%(region)s','%(address_gps_lat)s',
            '%(address_gps_lng)s','%(category_tags_l1_name)s','%(category_tags_l2_name)s','%(category_tags_l3_name)s','%(star_score)s','%(shop_score)s',
            '%(pro_score)s','%(env_score)s','%(ser_score)s','%(avg_spend)s','%(comment_cnt)s','%(comment_tags)s','%(create_time)s'
            )
        """ % kwargs
        try:
            cur.execute(sql)
            conn.commit()
            # pprint(kwargs)
            print('插入成功:',kwargs['id'],kwargs['shopname'])
        except Exception as e:
            # print(e)
            print('店铺已经存在:',kwargs['id'],kwargs['shopname'])
    def run(self):
        kwargs = self.pre_args_str()
        self.get_list('1',kwargs)
        if self.page_count != 1:
            print('总页数：',self.page_count)
            for page in range(2,self.page_count):
                print('当前页数---',page)
                self.get_list(page,kwargs)
if __name__ == '__main__':
    def work():
        while True:
            args = redis_cli.spop(redis_name)
            print(args)
            meishi = dp_meishi(args)
            meishi.run()
    for i in range(4):
        t = threading.Thread(target=work)
        t.start()
        sleep(2)