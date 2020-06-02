import requests
from setting import setting

redis_cli = setting['redis_cli']
redis_name = setting['redis_IP']

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
    redis_cli.sadd(proxy)

def check_ipNum():
    count = redis_cli.scard(redis_name)
    if int(count) < 2:
        taiyang_proxy()

def get_error():
    check_ipNum()

def get_ip():
    check_ipNum()
    return redis_cli.spop(redis_name)

def taiyang_proxy():
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=20681&port=11&lb=4&pb=45&regions=')

    ip_list = resp.content.decode().split('\n')
    for ip in ip_list:
        if len(ip) > 4:
            continue
        redis_cli.sadd(redis_name,ip)

if __name__ == '__main__':
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=20681&port=11&lb=4&pb=45&regions=')
    print(resp.text)