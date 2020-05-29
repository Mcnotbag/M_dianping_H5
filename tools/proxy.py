import requests




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

def taiyang_proxy():
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=20681&port=11&lb=4&pb=45&regions=')
    # print(resp.text)
    if '套餐已用完' in resp.text or '频繁' in resp.text:
        resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=50186&port=1&lb=1&pb=4&regions=')
    proxy =  {
        'http':'http://'+resp.text.replace('\n',''),
        'https':'https://'+resp.text.replace('\n','')
    }
    return proxy

if __name__ == '__main__':
    resp = requests.get('http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=20681&port=11&lb=4&pb=45&regions=')
    print(resp.text)