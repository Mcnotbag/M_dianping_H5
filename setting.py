import psycopg2
from fake_useragent import UserAgent
from redis import Redis

ua = UserAgent(path='tools/ua.json')

# 线上
conn = psycopg2.connect(database="crawler", user="root", password="9TTjkHY^Y#UeLORZ", host="10.101.0.90", port="8635")
# 本地
# conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="postgres", host="localhost", port="8635")
# 本地
# redis_cli = Redis(decode_responses=True)
# 线上
redis_cli = Redis(host='10.101.0.239',password='abc123',decode_responses=True)
redis_name = 'dp_ch50_shenzhen'

redis_IP_name = 'redis_IP'