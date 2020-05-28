import requests


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