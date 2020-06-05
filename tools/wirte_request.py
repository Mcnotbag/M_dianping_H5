import os
from redis import Redis


# 线上
redis_cli = Redis(host='10.101.0.239',password='abc123',decode_responses=True)
redis_name = 'dp_ch10_shenzhen'
def wirte_redis_request():
    cate_path = '../category/'
    region_path = '../region/深圳/'
    filenames = os.listdir(cate_path)
    for filename in filenames:
        category_2_id = filename.replace('.txt','').split('$')[0]
        category_2_title = filename.replace('.txt','').split('$')[1]
        with open(cate_path + filename,'r',encoding='utf-8') as f:
            category_3_list = f.read().split('\n')
            for category_3 in category_3_list:
                if category_3 == '':
                    continue
                category_3_id = category_3.split('$')[0]
                # category_3_id = '210'
                category_3_title = category_3.split('$')[0]
                for r in os.listdir(region_path):
                    put_str = filename.replace('.txt', '') + ';' + category_3 + ';' + r.replace('.txt','')
                    print(put_str)
                    redis_cli.sadd(redis_name,put_str)
                    with open(region_path + r,'r',encoding='utf-8') as f:
                        region_list = f.read().split('\n')
                        for region_str in region_list:
                            if region_str == '':
                                continue
                            put_str = filename.replace('.txt','') + ';' + category_3 + ';' + r.replace('.txt','') + ';' + region_str
                            print(put_str)
                            redis_cli.sadd(redis_name,put_str)

wirte_redis_request()