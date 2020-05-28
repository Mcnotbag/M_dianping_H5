import os

import requests


headers = {
'Accept': 'application/json, text/javascript',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
'Host': 'www.dianping.com',
'Origin': 'http://www.dianping.com',
'Referer': 'http://www.dianping.com/search/map/category/7/10/g112',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'X-Request': 'JSON',
'X-Requested-With': 'XMLHttpRequest',
}

data = {
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


def get_list(categoryId,regionId):
    # http://www.dianping.com/search/map/category/7/10/g112
    url = 'http://www.dianping.com/search/map/category/7/10/' + categoryId + regionId



def wirte_redis_request():
    path = 'category/'
    filenames = os.listdir(path)
    for filename in filenames:
        category_2_id = filename.replace('.txt','').split('$')[0]
        category_2_title = filename.replace('.txt','').split('$')[1]
        with open(path + filename,'r',encoding='utf-8') as f:
            category_3_list = f.read().split('\n')
            for category_3 in category_3_list:
                category_3_id = category_3.split('$')[0]
                category_3_title = category_3.split('$')[0]
                url = 'http://www.dianping.com/search/map/ajax/json'
                headers['Referer'] = 'http://www.dianping.com/search/map/category/7/10/' + category_3_id
                data['categoryId'] = category_3_id.replace('g','')
                response = requests.post(url,headers=headers,data=data)
                print(response.content.decode())
                break
        break
wirte_redis_request()



