#! -*- coding:utf-8 -*-
import json

import requests
from lxml import etree
import re
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import numpy
import os
from woff2tff import woff_to_ttf

# tessdata_dir_config = '--tessdata-dir "c://Program Files (x86)//Tesseract-OCR//tessdata"'

class DaZhongDianPing():
    def __init__(self):
        self.url = "http://www.dianping.com/shenzhen/ch10/g117"
        # 页面 html
        self.html = None
        # 页面引用的 css 文件
        self.css = None
        self.woff_dc = dict()
        self.address_font_map = dict()
        self.shop_num_font_map = dict()
        self.tag_name_font_map = dict()
        self.referer = self.url.replace('/review_all', '')
        self.timeout = 10
        # self.headers = {
        #       'Connection': 'keep-alive',
        #       'Pragma': 'no-cache',
        #       'Cache-Control': 'no-cache',
        #       'Upgrade-Insecure-Requests': '1',
        #       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        #       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #       'Accept-Language': 'zh-CN,zh;q=0.9',
        # }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'Referer': 'http://www.dianping.com/shenzhen/ch20/g2714',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
        }

    def get_woffs(self):
        html_res = requests.get(self.url, headers=self.headers)
        self.html = html_res.content.decode()
        result = re.search('<link rel="stylesheet" type="text/css" href="//s3plus(.*?)">', self.html, re.S)

        if result:
            css_url = 'http://s3plus' + result.group(1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            }
            css_res = requests.get(css_url, headers=headers)
            # print(css_url)
            self.css = css_res.content.decode()

            result = re.findall('@font-face\{font-family: "(.*?)";.*?,url\("(.*?)"\);\}', self.css)
            # print(result)

            self.woff_dc = dict(result)
            for woff_url in result:
                url = 'http:' + woff_url[1]
                res = requests.get(url, headers=headers)
                filename = woff_url[1].split('/')[-1]
                filepath = f'./woff_file/{filename}'
                with open(filepath, 'wb') as f:
                    f.write(res.content)
                self.woff_dc[woff_url[0]] = filepath

    def get_woff_2_ttf(self):
        tmp_dc = self.woff_dc
        for key in tmp_dc:
            woff_path = tmp_dc[key]
            ttf_filepath = woff_path.replace('.woff', '.ttf')
            woff_to_ttf([woff_path, ttf_filepath])
            self.woff_dc[key] = ttf_filepath

    def fontConvert(self, fontPath):
        fonts = TTFont(fontPath)
        codeList = fonts.getGlyphOrder()[2:]
        im = Image.new("RGB", (1800, 1000), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype(font=os.path.abspath(fontPath), size=40)
        count = 18
        arrayList = numpy.array_split(codeList, count)
        for t in range(count):
            newList = [i.replace("uni", "\\u") for i in arrayList[t]]
            text = "".join(newList)
            text = text.encode('utf-8').decode('unicode_escape')
            dr.text((0, 52 * t), text, font=font, fill="#000000")
        im.save("font.jpg")
        im = Image.open("font.jpg")
        result = pytesseract.image_to_string(im, lang="chi_sim")
        result = result.replace(" ", "").replace("\n", "").replace("'J\\",'小').replace('_',"一").replace('士蒯L','地儿').replace('熹','鑫').replace('到','卫').replace('‖','川')
        texts = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '0', '店', '中', '美', '家', '馆', '小', '车', '大',
            '市', '公', '酒', '行', '国', '品', '发', '电', '金', '心',
            '业', '商', '司', '超', '生', '装', '园', '场', '食', '有',
            '新', '限', '天', '面', '工', '服', '海', '华', '水', '房',
            '饰', '城', '乐', '汽', '香', '部', '利', '子', '老', '艺',
            '花', '专', '东', '肉', '菜', '学', '福', '饭', '人', '百',
            '餐', '茶', '务', '通', '味', '所', '山', '区', '门', '药',
            '银', '农', '龙', '停', '尚', '安', '广', '鑫', '一', '容',
            '动', '南', '具', '源', '兴', '鲜', '记', '时', '机', '烤',
            '文', '康', '信', '果', '阳', '理', '锅', '宝', '达', '地',
            '儿', '衣', '特', '产', '西', '批', '坊', '州', '牛', '佳',
            '化', '五', '米', '修', '爱', '北', '养', '卖', '建', '材',
            '三', '会', '鸡', '室', '红', '站', '德', '王', '光', '名',
            '丽', '油', '院', '堂', '烧', '江', '社', '合', '星', '货',
            '型', '村', '自', '科', '快', '便', '日', '民', '营', '和',
            '活', '童', '明', '器', '烟', '育', '宾', '精', '屋', '经',
            '居', '庄', '石', '顺', '林', '尔', '县', '手', '厅', '销',
            '用', '好', '客', '火', '雅', '盛', '体', '旅', '之', '鞋',
            '辣', '作', '粉', '包', '楼', '校', '鱼', '平', '彩', '上',
            '吧', '保', '永', '万', '物', '教', '吃', '设', '医', '正',
            '造', '丰', '健', '点', '汤', '网', '庆', '技', '斯', '洗',
            '料', '配', '汇', '木', '缘', '加', '麻', '联', '卫', '川',
            '泰', '色', '世', '方', '寓', '风', '幼', '羊', '烫', '来',
            '高', '厂', '兰', '阿', '贝', '皮', '全', '女', '拉', '成',
            '云', '维', '贸', '道', '术', '运', '都', '口', '博', '河',
            '瑞', '宏', '京', '际', '路', '祥', '青', '镇', '厨', '培',
            '力', '惠', '连', '马', '鸿', '钢', '训', '影', '甲', '助',
            '窗', '布', '富', '牌', '头', '四', '多', '妆', '吉', '苑',
            '沙', '恒', '隆', '春', '干', '饼', '氏', '里', '二', '管',
            '诚', '制', '售', '嘉', '长', '轩', '杂', '副', '清', '计',
            '黄', '讯', '太', '鸭', '号', '街', '交', '与', '叉', '附',
            '近', '层', '旁', '对', '巷', '栋', '环', '省', '桥', '湖',
            '段', '乡', '厦', '府', '铺', '内', '侧', '元', '购', '前',
            '幢', '滨', '处', '向', '座', '下', '県', '凤', '港', '开',
            '关', '景', '泉', '塘', '放', '昌', '线', '湾', '政', '步',
            '宁', '解', '白', '田', '町', '溪', '十', '八', '古', '双',
            '胜', '本', '单', '同', '九', '迎', '第', '台', '玉', '锦',
            '底', '后', '七', '斜', '期', '武', '岭', '松', '角', '纪',
            '朝', '峰', '六', '振', '珠', '局', '岗', '洲', '横', '边',
            '济', '井', '办', '汉', '代', '临', '弄', '团', '外', '塔',
            '杨', '铁', '浦', '字', '年', '岛', '陵', '原', '梅', '进',
            '荣', '友', '虹', '央', '桂', '沿', '事', '津', '凯', '莲',
            '丁', '秀', '柳', '集', '紫', '旗', '张', '谷', '的', '是',
            '不', '了', '很', '还', '个', '也', '这', '我', '就', '在',
            '以', '可', '到', '错', '没', '去', '过', '感', '次', '要',
            '比', '觉', '看', '得', '说', '常', '真', '们', '但', '最',
            '喜', '哈', '么', '别', '位', '能', '较', '境', '非', '为',
            '欢', '然', '他', '挺', '着', '价', '那', '意', '种', '想',
            '出', '员', '两', '推', '做', '排', '实', '分', '间', '甜',
            '度', '起', '满', '给', '热', '完', '格', '荐', '喝', '等',
            '其', '再', '几', '只', '现', '朋', '候', '样', '直', '而',
            '买', '于', '般', '豆', '量', '选', '奶', '打', '每', '评',
            '少', '算', '又', '因', '情', '找', '些', '份', '置', '适',
            '什', '蛋', '师', '气', '你', '姐', '棒', '试', '总', '定',
            '啊', '足', '级', '整', '带', '虾', '如', '态', '且', '尝',
            '主', '话', '强', '当', '更', '板', '知', '己', '无', '酸',
            '让', '入', '啦', '式', '笑', '赞', '片', '酱', '差', '像',
            '提', '队', '走', '嫩', '才', '刚', '午', '接', '重', '串',
            '回', '晚', '微', '周', '值', '费', '性', '桌', '拍', '跟',
            '块', '调', '糕'
        ]
        codeList = [i.replace("uni", "&#x") + ";" for i in codeList]
        return dict(zip(codeList, texts))

    def get_font_map(self):
        for key in self.woff_dc:
            json_filename = self.woff_dc[key].split('/')[-1].split('.')[0] + '.json'
            json_filename_list = [i for i in os.listdir('woff_file') if '.json' in i]
            if 'shopNum' in key:
                if json_filename in json_filename_list:
                    with open('woff_file/'+json_filename,'r',encoding='utf-8') as f:
                        self.shop_num_font_map = json.loads(f.read())
                else:
                    self.shop_num_font_map = self.fontConvert(self.woff_dc[key])
                    with open('woff_file/'+json_filename,'w',encoding='utf-8') as f:
                        f.write(json.dumps(self.shop_num_font_map))
            elif 'address' in key:
                if json_filename in json_filename_list:
                    with open('woff_file/'+json_filename,'r',encoding='utf-8') as f:
                        self.address_font_map = json.loads(f.read())
                else:
                    self.address_font_map = self.fontConvert(self.woff_dc[key])
                    with open('woff_file/'+json_filename,'w',encoding='utf-8') as f:
                        f.write(json.dumps(self.address_font_map))

            elif 'tagName' in key:
                if json_filename in json_filename_list:
                    with open('woff_file/'+json_filename,'r',encoding='utf-8') as f:
                        self.tag_name_font_map = json.loads(f.read())
                else:
                    self.tag_name_font_map = self.fontConvert(self.woff_dc[key])
                    with open('woff_file/'+json_filename,'w',encoding='utf-8') as f:
                        f.write(json.dumps(self.tag_name_font_map))


    def get_shop_info(self):
        shopNum_res = re.findall('<svgmtsi class="shopNum">(.*?)</svgmtsi>', self.html, re.S)
        for i in shopNum_res:
            self.html = re.sub('<svgmtsi class="shopNum">{}</svgmtsi>'.format(i), self.shop_num_font_map[i], self.html)

        address_res = re.findall('<svgmtsi class="address">(.*?)</svgmtsi>', self.html, re.S)

        for i in address_res:
            self.html = re.sub('<svgmtsi class="address">{}</svgmtsi>'.format(i), self.address_font_map[i], self.html)


        tagName = re.findall('<svgmtsi class="tagName">(.*?)</svgmtsi>', self.html, re.S)
        for i in tagName:
            self.html = re.sub('<svgmtsi class="tagName">{}</svgmtsi>'.format(i), self.tag_name_font_map[i], self.html)

        tree = etree.HTML(self.html)
        shop_title_list = tree.xpath('//div[@class="tit"]/a/h4/text()')
        shop_star_score = tree.xpath('//div[@class="comment"]/div/div[2]/text()')
        shop_review_nums = tree.xpath('//div[@class="comment"]/a[1]/b/text()')
        shop_mean_price = tree.xpath('//div[@class="comment"]/a[2]/b/text()')
        shop_tag = tree.xpath('//div[@class="tag-addr"]/a[1]/span/text()')
        shop_address_tag = tree.xpath('//div[@class="tag-addr"]/a[2]/span/text()')
        shop_adress_des = tree.xpath('//div[@class="tag-addr"]/span/text()')
        shop_taste_score = tree.xpath('//span[@class="comment-list"]/span[1]/b/text()')
        shop_environment_score = tree.xpath('//span[@class="comment-list"]/span[2]/b/text()')
        shop_server_score = tree.xpath('//span[@class="comment-list"]/span[3]/b/text()')
        shop_recommend_dishes = tree.xpath('//div[@class="recommend"]/a/text()')

        print(shop_title_list)
        print(shop_star_score)
        print(shop_review_nums)
        print(shop_mean_price)
        print(shop_tag)
        print(shop_address_tag)
        print(shop_adress_des)
        print(shop_taste_score)
        print(shop_environment_score)
        print(shop_server_score)
        print(shop_recommend_dishes)

    def run(self):
        self.get_woffs()
        self.get_woff_2_ttf()
        self.get_font_map()
        self.get_shop_info()

    def work(self):
        pass

if __name__ == '__main__':
    dz = DaZhongDianPing()
    dz.run()
