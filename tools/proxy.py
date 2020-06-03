import random

import requests
from setting import *



def abuyun():
    # 要访问的目标页面
    targetUrl = "http://test.abuyun.com"
    #targetUrl = "http://proxy.abuyun.com/switch-ip"
    #targetUrl = "http://proxy.abuyun.com/current-ip"

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HB987O3119H4SKND"
    proxyPass = "043294EA6D42D52A"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    return proxies


def get_success(proxy):
    mapping = {
        proxy:1
    }
    redis_cli.zadd(redis_IP_name,mapping)

def check_ipNum():
    count = redis_cli.zcount(redis_IP_name,0,1)
    if int(count) < 5:
        taiyang_proxy()

def get_error(proxy):
    score = redis_cli.zscore(redis_IP_name,proxy)
    if score == 0:
        mapping = {proxy:-1}
    else:
        mapping = {proxy:0}
    redis_cli.zadd(redis_IP_name,mapping)
    check_ipNum()

def get_ip():
    count = redis_cli.zcount(redis_IP_name,0,1)
    if int(count) == 0:
        check_ipNum()
    proxies = redis_cli.zrange(redis_IP_name,0,-1,withscores=True)
    while True:
        proxy,score = random.choice(proxies)
        if score != -1:
            break
    return proxy


def taiyang_proxy():
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=5&type=1&pack=20681&port=1&lb=4&pb=45&regions=440000')
    ip_list = resp.text.split('\n')
    for ip in ip_list:
        if len(ip) < 2:
            continue
        mapping = {ip:1}
        redis_cli.zadd(redis_IP_name,mapping)
        print('添加ip到池:',ip)

if __name__ == '__main__':
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=20681&port=11&lb=4&pb=45&regions=')
    print(resp.text)