#coding:utf-8
import hashlib
import json
import os
import random
import threading
from datetime import datetime
from pprint import pprint
from time import sleep, time
from setting import *
import psycopg2
import requests
from redis import Redis

from tools.proxy import *
from get_shop_comment import Shop_Comment
from fake_useragent import UserAgent

cur = conn.cursor()
# 本地
# redis_cli = Redis(decode_responses=True)
# 线上

def enpytro():
    s = hex(int(65536 * (1 + random.random())))
    return s.replace('0x','')[1:]

def get_hc_v():
    return enpytro() + enpytro() + "-" + enpytro() + "-" + enpytro() + "-" + enpytro() + "-" + enpytro() + enpytro() + enpytro() + '.' + str(int(time()))



class dp_meishi:
    def __init__(self,dp_args):
        # self.city_name = '广州市'
        # self.city_en_name = ''
        # self.cityId = ''
        self.chtype = '10'
        self.chtype_name = '美食'
        self.proxy = get_ip()
        self.g_id = None
        self.r_id = None
        # self.page = 1
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
        'Referer': 'http://www.dianping.com/search/map/category/7/20/g112',
        'User-Agent': ua.random,
        # 'Cookie': 's_ViewType=10; _lxsdk_cuid=17263a5f11cc8-0a35404038c5e8-f7d1d38-1fa400-17263a5f11c6f',
            'Cookie':"_hc.v={};s_ViewType=10;".format(get_hc_v()),
        'X-Request': 'JSON',
        'X-Requested-With': 'XMLHttpRequest',
        }

    def get_list(self,kwargs):
        self.headers['Referer'] = f'http://www.dianping.com/search/map/category/{self.cityId}/{self.chtype}/{self.g_id}'
        self.data['categoryId'] = self.g_id.replace('g', '')
        self.data['regionId'] = self.r_id.replace('r','').replace('c','')
        self.data['page'] = self.page
        try:
            proxies = self.pre_proxy(self.proxy)
            response = requests.post(self.list_url, headers=self.headers, data=self.data,proxies=proxies,verify=False,timeout=10)
        except:
            get_error(self.proxy)
            self.proxy = get_ip()
            response = requests.post(self.list_url, headers=self.headers, data=self.data,verify=False,timeout=10)
        # print(response.content.decode())
        if response.status_code == 200:
            try:
                json_resp = json.loads(response.content.decode())
            except Exception as e:
                print(response.content.decode())
                raise e
            if json_resp['code'] == 200:
                # 将ip添加回ip池
                get_success(self.proxy)
                if self.page == 1:
                    self.page_count = json_resp['pageCount']
                    if self.page_count > 50:
                        self.page_count = 50
                for page in range(2,self.page_count):
                    args_str = self.args.split(';')[:-1] + ';' + str(page)
                    redis_cli.sadd(redis_name,args_str)
                for shop in json_resp['shopRecordBeanList']:
                    # 去重过滤
                    if redis_cli.sismember(redis_filter_name,shop['shopId']):
                        # print('这家店铺已存在-------：',shop['shopName'])
                        continue
                    kwargs['shopid'] = shop['shopId']
                    kwargs['shopname'] = shop['shopName'].replace("'",'‘')
                    kwargs['shop_score'] = shop['shopPower']
                    kwargs['star_score'] = shop['shopPowerTitle']
                    kwargs['url'] = 'http://www.dianping.com/shop/'+ shop['shopId']
                    kwargs['address_gps_lng'] = shop['geoLng']
                    kwargs['address_gps_lat'] = shop['geoLat']
                    kwargs['address'] = shop['address'].replace("'","")
                    kwargs['avg_spend'] = shop['avgPrice']
                    # sleep(random.uniform(0.2,0.5))
                    # print(kwargs['url']+ '/review_all')

                    detail_obj = Shop_Comment(kwargs['url']+ '/review_all',proxy=self.pre_proxy(self.proxy))
                    info_kwargs,comm_kwargs_list = detail_obj.run()
                    if info_kwargs == {}:
                        kwargs['comment_cnt'] = '0'
                        kwargs['comment_tags'] = ''
                        kwargs['pro_score'] = ''
                        kwargs['env_score'] = ''
                        kwargs['ser_score'] = ''
                    kwargs.update(info_kwargs)
                    kwargs = self.clean_kwargs(**kwargs)
                    self.insert_shop_info(**kwargs)
                    self.insert_comment(comm_kwargs_list)
                    # 添加到过滤池
                    redis_cli.sadd(redis_filter_name,kwargs['shopid'])
            else:
                print('code 不是200：--------',json_resp['code'])
                if json_resp['code'] != 500:
                    get_success(self.proxy)
                    self.proxy = get_ip()
                    if self.page > 1:
                        redis_cli.sadd(redis_name, self.args)
                # 如果翻页到50以后，不能将IP认定为不能使用
                # if self.page < 50:
                #     # get_error(self.proxy)
                #     get_success(self.proxy)
                #     self.proxy = get_ip()
                # elif 50 < self.page < 100:
                #     get_success(self.proxy)
                #     self.proxy = get_ip()

        else:
            print('状态码不是200：,',response.status_code)
            redis_cli.sadd(redis_name,self.args)
            get_error(self.proxy)
            self.proxy = get_ip()
        # print('当前IP：', self.proxy)

    def pre_proxy(self,proxy):
        return {
        'http':'http://'+proxy.replace('\n',''),
        'https':'https://'+proxy.replace('\n','')
    }

    def pre_args_str(self):
        kwargs = {}
        dp_args = self.args
        kwargs['source_data'] = '大众点评'
        kwargs['category_tags_l1_name'] = self.chtype_name
        kwargs['category_tags_l2_name'] = dp_args.split(';')[0].split('$')[1]
        kwargs['category_tags_l3_name'] = dp_args.split(';')[1].split('$')[1]
        self.g_id = dp_args.split(';')[1].split('$')[0]
        kwargs['city'] = dp_args.split(';')[-2].split('$')[0] + '市'
        self.city_en_name = dp_args.split(';')[-2].split('$')[-1]
        self.cityId = dp_args.split(';')[-2].split('$')[1]
        self.page = int(dp_args.split(';')[-1])
        kwargs['district'] = dp_args.split(';')[2].split('$')[1]
        if len(dp_args.split(';')) == 5:
            kwargs['region'] = ''
            self.r_id = dp_args.split(';')[2].split('$')[0]
        else:
            kwargs['region'] = dp_args.split(';')[3].split('$')[1]
            self.r_id = dp_args.split(';')[3].split('$')[0]

        self.data = {
            'cityId': self.cityId,
            'cityEnName': self.city_en_name,
            'promoId': '0',
            'shopType': self.chtype,
            'categoryId': '112',
            'regionId': '0',
            'sortMode': '2', # 1 按价钱低到高 Item 8;
            'shopSortItem': '2', # 2 按人气 ；3 按总体；11 按评论数；9 价格高到低； 0 默认；
            'keyword': '',
            'searchType': '1',
            'branchGroupId': '0',
            'aroundShopId': '0',
            'shippingTypeFilterValue': '0',
            'page': '1',
        }

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
            kwargs['env_score'] = kwargs['env_score'].replace('环境：','').replace('做工工艺：','').replace('服务：','').replace('做工品质：','')
        except Exception as e:
            kwargs['env_score'] = 0
        if kwargs['env_score'] == '':
            kwargs['env_score'] = 0
        # 口味评分
        try:
            kwargs['pro_score'] = kwargs['pro_score'].replace('口味：','').replace('款式设计：','').replace('效果：','').replace('产品：','').replace('设施：','').replace('服务：','').replace('颜色款式：','')
        except Exception as e:
            kwargs['pro_score'] = 0
        if kwargs['pro_score'] == '':
            kwargs['pro_score'] = 0
        # 服务评分
        try:
            kwargs['ser_score'] = kwargs['ser_score'].replace('服务：','').replace('环保材质：','').replace('设施配置：','').replace('安装服务：','')
        except Exception as e:
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
            insert into dianping_beauty.dianping_comment values ('%(id)s','%(shopid)s','%(shopname)s','%(comment)s','%(url)s','%(user_name)s','%(user_level)s','%(user_vip)s','%(pro_score)s',
            '%(env_score)s','%(ser_score)s','%(com_date)s','%(create_time)s','%(shop_score)s')
            """ % comment
            try:
                cur.execute(sql)
                conn.commit()
            except Exception as e:
                # print('评论已存在',comment['id'],'店名:',comment['shopname'])
                if e.__class__ == psycopg2.errors.UniqueViolation or e.__class__ == psycopg2.errors.InFailedSqlTransaction:
                    # conn.commit()
                    conn.rollback()
                else:
                    print('sql:', sql)
                    print('error:',e)
                    conn.rollback()
        # print('评论插入成功：')

    def insert_shop_info(self,**kwargs):
        sql = """
            insert into dianping_beauty.dianping_shop values (
            '%(source_data)s','%(id)s','%(shopname)s','%(shopid)s','%(url)s','%(address)s','%(city)s','%(district)s','%(region)s','%(address_gps_lat)s',
            '%(address_gps_lng)s','%(category_tags_l1_name)s','%(category_tags_l2_name)s','%(category_tags_l3_name)s','%(star_score)s','%(shop_score)s',
            '%(pro_score)s','%(env_score)s','%(ser_score)s','%(avg_spend)s','%(comment_cnt)s','%(comment_tags)s','%(create_time)s'
            )
        """ % kwargs
        try:
            cur.execute(sql)
            conn.commit()
            # pprint(kwargs)
            # print('插入成功:',kwargs['id'],kwargs['shopname'])
        except Exception as e:
            if e.__class__ == psycopg2.errors.UniqueViolation or e.__class__ == psycopg2.errors.InFailedSqlTransaction:
                conn.rollback()
                # conn.commit()
                # print(e)
            else:
                print('sql:',sql)
                raise e
            # print('店铺已经存在:',kwargs['id'],kwargs['shopname'])
    def run(self):
        kwargs = self.pre_args_str()
        self.get_list(kwargs)
        print('总页数：', self.page_count)
        if self.page_count > 1:
            for self.page in range(2,self.page_count):
                print('当前页数---',self.page)
                self.get_list(kwargs)
if __name__ == '__main__':
    def work():
        while redis_cli.scard(redis_name):
            args = redis_cli.spop(redis_name)
            print(args)
            meishi = dp_meishi(args)
            meishi.run()
    # work()
    for i in range(4):
        t = threading.Thread(target=work)
        t.start()
        sleep(random.uniform(1,2))