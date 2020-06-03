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
    redis_cli.sadd(redis_IP_name,proxy)

def check_ipNum():
    count = redis_cli.scard(redis_IP_name)
    if int(count) < 5:
        taiyang_proxy()

def get_error(proxy):
    redis_cli.sadd(redis_IP_name,proxy)
    check_ipNum()

def get_ip():
    count = redis_cli.scard(redis_IP_name)
    if int(count) == 0:
        check_ipNum()
    return redis_cli.spop(redis_IP_name)

def taiyang_proxy():
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=5&type=1&pack=20681&port=1&lb=4&pb=45&regions=440000')
    ip_list = resp.text.split('\n')
    for ip in ip_list:
        if len(ip) < 2:
            continue
        redis_cli.sadd(redis_IP_name,ip)
        print('添加ip到池:',ip)

if __name__ == '__main__':
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=20681&port=11&lb=4&pb=45&regions=')
    print(resp.text)