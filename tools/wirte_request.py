import os
from redis import Redis


redis_cli = Redis(decode_responses=True)
redis_name = 'dp_ch10'
def wirte_redis_request():
    cate_path = '../category/'
    region_path = '../region/'
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
                put_str = filename.replace('.txt','') + ';' + category_3 + ';' + 'r31$南山区'
                print(put_str)
                redis_cli.sadd(redis_name,put_str)
                with open(region_path + 'r31$南山区.txt','r',encoding='utf-8') as f:
                    region_list = f.read().split('\n')
                    for region_str in region_list:
                        if region_str == '':
                            continue
                        put_str = filename.replace('.txt','') + ';' + category_3 + ';' + 'r31$南山区' + ';' + region_str
                        print(put_str)
                        redis_cli.sadd(redis_name,put_str)

wirte_redis_request()