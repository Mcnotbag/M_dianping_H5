#coding:utf-8
import hashlib
from datetime import datetime
from pprint import pprint

import psycopg2
import requests
import re
import time
from lxml import etree
import random

# conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="postgres", host="localhost", port="8635")
# cur = conn.cursor()

class Shop_Comment():
    def __init__(self,shop_url,proxy):
        self.proxy = proxy
        self.kwargs = {}
        self.comment_list = []
        self.url = shop_url
        # 页面 html
        self.html = None
        # 页面字体大小
        self.font_size = 14
        # 页面引用的 css 文件
        self.css = None
        # 商家地址使用的 svg 文件
        self.address_svg = None
        # 商家电话使用的 svg 文件
        self.tell_svg = None
        # 商家评论使用的 svg 文件
        self.review_svg = None

        # 字体码表，key 为 class 名称，value 为对应的汉字
        self.address_font_map = dict()
        self.tell_font_map = dict()
        self.review_font_map = dict()

        # 商家评论的最大页码数
        self.max_pages = None
        self.referer = self.url.replace('/review_all', '')
        self.timeout = 10
        self.headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': self.referer,
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': ''
        }
    # 目前不用
    # def get_max_pages(self):
    #     tree = etree.HTML(self.html)
    #     self.max_pages = int(tree.xpath('//div[@class="reviews-pages"]/a/text()')[-2])

    def get_svg_html(self):
        # 获取商家评论页内容
        try:
            index_res = requests.get(self.url, headers=self.headers,timeout=self.timeout,verify=False,proxies=self.proxy)
        except:
            index_res = requests.get(self.url, headers=self.headers, timeout=self.timeout, verify=False)
        self.html = index_res.text

        # 正则匹配 css 文件
        result = re.search('<link rel="stylesheet" type="text/css" href="//s3plus(.*?)">', self.html, re.S)
        if result:
            css_url = 'http://s3plus' + result.group(1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            }
            css_res = requests.get(css_url, headers=headers)
            # print(f'css_url:{css_url}')
            self.css = css_res.text

            # 正则匹配商家地址使用的 svg 文件 url
            """
            result = re.search('bb\[class.*?background-image: url\((.*?)\);', self.css, re.S)
            address_svg_url = 'http:' + result.group(1)
            self.address_svg = requests.get(address_svg_url, headers=headers).text
            print(f'address_svg_url:{address_svg_url}')

            # 正则匹配商家电话号码使用的 svg 文件 url
            result = re.search('cc\[class.*?background-image: url\((.*?)\);', self.css, re.S)
            tell_svg_url = 'http:' + result.group(1)
            self.tell_svg = requests.get(tell_svg_url, headers=headers).text
            print(f'tell_svg_url:{tell_svg_url}')
            """
            # 正则匹配评论使用的 svg 文件 url
            result = re.search('svgmtsi\[class.*?background-image: url\((.*?)\);', self.css, re.S)
            # print(result)
            review_svg_url = 'http:' + result.group(1)
            self.review_svg = requests.get(review_svg_url, headers=headers).text
            # print(review_svg_url)

    def get_font_map(self):
        # <bb class="xxx.*?"></bb>              地址
        # <cc class="xxx.*?"></cc>              电话
        # <svgmtsi class="xxx.*?"></svgmtsi>    评论
        # xxx 每天都会发生变化，所以动态匹配对应的前缀

        result = re.search('<bb class="(.*?)"></bb>', self.html, re.S)
        # address_prefix = result.group(1)[:2]

        result = re.search('<cc class="(.*?)"></cc>', self.html, re.S)
        # tell_prefix = result.group(1)[:2]

        result = re.search('<svgmtsi class="(.*?)"></svgmtsi>', self.html, re.S)
        try:
            review_prefix = result.group(1)[:2]
        except:
            # print('关注下这个页面，没有数据',self.url)
            return False


        """
        匹配 css 文件中格式为 '.' + self.prefix + (.*?){background:(.*?)px (.*?)px;} 的 css 样式

        匹配 svg 文件中格式为 <path id="(\d+)" d="M0 (\d+) H600"/> 的字段，其中 id 的值对应 xlink:href="#(\d+)" 的值，
        d="M0 (\d+) H600" 的值对应 background中 y轴的偏移量

        匹配 svg 文件中格式为 <textPath xlink:href="#(\d+)" textLength=".*?">(.*?)</textPath> 的字段，(.*?) 对应一串中文字符串，
        最终的字符 = 中文字符串[x轴偏移量 / 字体大小]
        :return:
        """

        # 地址css标签
        # address_class_list = re.findall('\.%s(.*?){background:(.*?)px (.*?)px;}' % address_prefix, self.css, re.S)
        # 电话css标签
        # tell_class_list = re.findall('\.%s(.*?){background:(.*?)px (.*?)px;}' % tell_prefix, self.css, re.S)
        # 评论css标签
        review_class_list = re.findall('\.%s(.*?){background:(.*?)px (.*?)px;}' % review_prefix, self.css, re.S)

        # 地址偏移
        # address_svg_y_list = re.findall('<path id="(\d+)" d="M0 (\d+) H600"/>', self.address_svg, re.S)

        review_svg_y_words = re.findall('<text x=".*?" y="(.*?)">(.*?)</text>', self.review_svg, re.S)
        if not review_svg_y_words:
            review_svg_y_list = re.findall('<path id="(\d+)" d="M0 (\d+) H600"/>', self.review_svg, re.S)
            review_result = re.findall('<textPath xlink:href="#(\d+)" textLength=".*?">(.*?)</textPath>',
                                       self.review_svg, re.S)
            review_words_dc = dict(review_result)
            self.review_font_map = self.address_class_to_font(review_class_list, review_svg_y_list, review_words_dc, review_prefix)
        else:
            self.review_font_map = self.review_class_to_font(review_class_list, review_svg_y_words, review_prefix)
        #地址
        # address_result = re.findall('<textPath xlink:href="#(\d+)" textLength=".*?">(.*?)</textPath>', self.address_svg, re.S)
        #电话
        # tell_result = re.search('<text x="(.*?)" y=".*?">(.*?)</text>', self.tell_svg, re.S)
        # tell_x_list = tell_result.group(1).split(' ')
        # tell_words_str = tell_result.group(2)

        # address_words_dc = dict(address_result)
        # self.address_font_map = self.address_class_to_font(address_class_list, address_svg_y_list, address_words_dc, address_prefix)
        # self.tell_font_map = self.tell_class_to_num(tell_class_list, tell_x_list, tell_words_str, tell_prefix)
        # print(self.address_font_map)
        # print(self.review_font_map)
        # print(self.tell_font_map)
        return True

    def review_class_to_font(self, class_list, y_words, prefix):
        tmp_dc = dict()
        tmp = None
        for cname, x, y in class_list:
            for text_y, text in y_words:
                if int(text_y) >= abs(int(float(y))):
                    index = abs(int(float(x))) // self.font_size
                    tmp = text[index]
                    break
            tmp_dc[prefix + cname] = tmp
        return tmp_dc


    def address_class_to_font(self, class_list, y_list, words_dc, prefix):
        tmp_dc = dict()
        # 核心算法，将 css 转换为对应的字符
        for i in class_list:
            x_id = None
            for j in y_list:
                if int(j[1]) >= abs(int(float(i[2]))):
                    x_id = j[0]
                    break
            index = abs(int(float(i[1]))) // self.font_size
            tmp = words_dc[x_id][int(index)]
            tmp_dc[prefix + i[0]] = tmp
        return tmp_dc

    def tell_class_to_num(self, class_list, x_list, words_str, prefix):
        tmp_dc = dict()
        for i in class_list:
            x_index = None
            for index, num in enumerate(x_list):
                if int(num) >= abs(int(float(i[1]))):
                    x_index = index
                    break
            tmp = words_str[x_index]
            tmp_dc[prefix + i[0]] = tmp
        return tmp_dc

    def get_shop_info(self):
        # 将 self.html 商铺地址加密的 class 样式替换成对应的中文字符
        # address_class_set = re.findall('<bb class="(.*?)"></bb>', self.html, re.S)
        # for class_name in address_class_set:
        #     self.html = re.sub('<bb class="{}"></bb>'.format(class_name), self.address_font_map[class_name], self.html)

        # 将 self.html 电话号码加密的 class 样式替换成对应的数字
        # tell_class_set = re.findall('<cc class="(.*?)"></cc>', self.html, re.S)
        # for class_name in tell_class_set:
        #     self.html = re.sub('<cc class="{}"></cc>'.format(class_name), self.tell_font_map[class_name], self.html)
        #
        # tree = etree.HTML(self.html)
        # shop_address = tree.xpath('//div[@class="address-info"]/text()')[0].replace('&nbsp;','').replace('\n','').replace(' ', '')
        # shop_tell = tree.xpath('//div[@class="phone-info"]/text()')[0].replace('&nbsp;','').replace('\n','').replace(' ', '')
        #
        # print(f'地址：{shop_address}\n电话：{shop_tell}')
        tree = etree.HTML(self.html)
        # comm_kwargs['shopname'] = ''.join(tree.xpath('//div[@class="review-shop-wrap"]/div[@class="shop-info clearfix"]/h1[@class="shop-name"]/text()')).replace("'","’")
        self.kwargs['comment_cnt'] = ''.join(tree.xpath("//div[@class='rank-info']//span[@class='reviews']/text()"))
        # avg_speed = ''.join(tree.xpath("//div[@class='rank-info']//span[@class='price']/text()"))
        # self.kwargs['pro_score'] = ''.join(tree.xpath("//div[@class='rank-info']//span[@class='score']/span[1]/text()"))
        # self.kwargs['env_score'] = ''.join(tree.xpath("//div[@class='rank-info']//span[@class='score']/span[2]/text()"))
        # self.kwargs['ser_score'] = ''.join(tree.xpath("//div[@class='rank-info']//span[@class='score']/span[3]/text()"))
        self.kwargs['pro_score'] = ''.join(re.findall(r'\w+：(.{3})',''.join(tree.xpath("//div[@class='rank-info']//span[@class='score']/span[1]/text()"))))
        self.kwargs['env_score'] = ''.join(re.findall(r'\w+：(.{3})', ''.join(tree.xpath("//div[@class='rank-info']//span[@class='score']/span[2]/text()"))))
        self.kwargs['ser_score'] = ''.join(re.findall(r'\w+：(.{3})', ''.join(tree.xpath("//div[@class='rank-info']//span[@class='score']/span[3]/text()"))))
        self.kwargs['comment_tags'] = ';'.join(tree.xpath('//div[@class="reviews-tags"]/div[@class="content"]/span/a/@date-type'))


    def get_user_info(self,is_sub):
        if is_sub:
            # 将 self.html 评论区域加密的 class 样式替换成对应的中文字符
            review_class_set = re.findall('<svgmtsi class="(.*?)"></svgmtsi>', self.html, re.S)
            for class_name in review_class_set:
                self.html = re.sub('<svgmtsi class="{}"></svgmtsi>'.format(class_name), self.review_font_map[class_name],
                                   self.html)

        xhtml = etree.HTML(self.html)
        comm_li = xhtml.xpath('//div[@class="reviews-items"]/ul/li/div[@class="main-review"]')
        for comm in comm_li:
            comm_kwargs = {}
            # 获取用户昵称
            comm_kwargs['user_name'] = ''.join(comm.xpath('./div[@class="dper-info"]/a/text()')).replace('\n','').replace(' ','')
            # 用户等级
            comm_kwargs['user_level'] = ''.join(comm.xpath('./div[@class="dper-info"]/img/@src')).split('/')[-1].replace('square','').replace('.png','')
            # 是否vip
            user_vip = comm.xpath('./div[@class="dper-info"]/span[@class="vip"]')
            if user_vip == []:
                comm_kwargs['user_vip'] = False
            else:
                comm_kwargs['user_vip'] = True
            # 店名
            comm_kwargs['shopname'] = ''.join(xhtml.xpath('//div[@class="review-shop-wrap"]/div[@class="shop-info clearfix"]/h1[@class="shop-name"]/text()')).replace("'", "’")
            # 评分
            try:
                comm_kwargs['shop_score'] = float(''.join(comm.xpath('./div[@class="review-rank"]/span[1]/@class')).replace('sml-rank-stars sml-str','').replace(' star',''))
            except Exception as e:
                comm_kwargs['shop_score'] = 0
            # comm_kwargs['pro_score'] = ''.join(comm.xpath('./div[@class="review-rank"]/span[@class="score"]/span[1]/text()')).replace('\n','').replace(' ','').replace('口味：','').replace('款式设计：','').replace('效果：','').replace('设施：','').replace('产品：','').replace('服务：','').replace('颜色款式：','')
            # comm_kwargs['env_score'] = ''.join(comm.xpath('./div[@class="review-rank"]/span[@class="score"]/span[2]/text()')).replace('\n','').replace(' ','').replace('环境：','').replace('做工工艺：','').replace('服务：','').replace('做工品质：','')
            # comm_kwargs['ser_score'] = ''.join(comm.xpath('./div[@class="review-rank"]/span[@class="score"]/span[3]/text()')).replace('\n','').replace(' ','').replace('服务：','').replace('环保材质：','').replace('设施配置：','').replace('安装服务：','')
            comm_kwargs['pro_score'] = ''.join(re.findall(r'\w+：(.{3})',''.join(comm.xpath('./div[@class="review-rank"]/span[@class="score"]/span[1]/text()'))))
            comm_kwargs['env_score'] = ''.join(re.findall(r'\w+：(.{3})', ''.join(comm.xpath('./div[@class="review-rank"]/span[@class="score"]/span[2]/text()'))))
            comm_kwargs['ser_score'] = ''.join(re.findall(r'\w+：(.{3})', ''.join(comm.xpath('./div[@class="review-rank"]/span[@class="score"]/span[3]/text()'))))

            # 处理评分
            if comm_kwargs['pro_score'] == '':
                comm_kwargs['pro_score'] = 0
            if comm_kwargs['env_score'] == '':
                comm_kwargs['env_score'] = 0
            if comm_kwargs['ser_score'] == '':
                comm_kwargs['ser_score'] = 0

            # 获取用户评论
            # comm_kwargs['comment'] = ''.join(comm.xpath('./div[@class="review-words Hide"]/text()')).replace(' ', '').replace('⃣', '.').replace('\n', '').replace('收起评论', '').replace("'",'’')
            # review_list = [i.xpath('string(.)').replace(' ', '').replace('⃣', '.').replace('\n', '').replace('收起评论', '') for
            #                i in user_review]
            comments = comm.xpath('./div[@class="review-words Hide"]')[0] if comm.xpath('./div[@class="review-words Hide"]') != [] else comm.xpath('.//div[@class="review-words"]')[0]

            comm_kwargs['comment'] = comments.xpath('string(.)').replace(' ', '').replace('⃣', '.').replace('\n', '').replace('收起评论', '').replace('\t','').replace("'",'’')

            # print(comments['comment'])
            # 评论时间
            comm_kwargs['com_date'] =''.join(comm.xpath('div[@class="misc-info clearfix"]/span[@class="time"]/text()')).replace('\n','').strip()
            if '更新' in comm_kwargs['com_date']:
                comm_kwargs['com_date'] = comm_kwargs['com_date'].split('更新于')[-1]
            comm_kwargs['url'] = self.url
            comm_kwargs['create_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            comm_kwargs['shopid'] = self.referer.split('/')[-1]
            # id user_name + $ + com_date
            hash_str = comm_kwargs['user_name'] + '$' + comm_kwargs['com_date']
            comm_kwargs['id'] = hashlib.md5(hash_str.encode('utf-8')).hexdigest()
            self.comment_list.append(comm_kwargs)

    # def insert_comment(self,comment_list):
    #     sql = """
    #     insert into dianping_comment values (%(id)s,%(shopid)s,%(shopname)s,%(comment)s,%(url)s,%(user_name)s,%(user_level)s,%(user_vip)s,%(pro_score)s,
    #     %(env_score)s,%(ser_score)s,%(com_date)s,%(create_time)s,%(shop_score)s)
    #     """
    #     cur.executemany(sql,comment_list)
    #     conn.commit()
            # try:
            #     cur.execute(sql)
            #     conn.commit()
            # except Exception as e:
            #     # print('评论已存在',comment['id'],'店名:',comment['shopname'])
            #     if e.__class__ == psycopg2.errors.UniqueViolation or e.__class__ == psycopg2.errors.InFailedSqlTransaction:
            #         pass
            #     else:
            #         print('sql:', sql)
            #         raise e


    def run(self):
        self.kwargs = {}
        self.get_svg_html()
        # self.get_max_pages()
        result = self.get_font_map()

        self.get_shop_info()
        self.get_user_info(result)
        return self.kwargs,self.comment_list
if __name__ == '__main__':
    dz = Shop_Comment('http://www.dianping.com/shop/HazCP8g4dlSq1pUa/review_all','')
    dz.run()
