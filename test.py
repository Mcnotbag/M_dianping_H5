#coding:utf-8
import json
import os

import psycopg2
import redis
import requests
from fake_useragent import UserAgent
# from setting import ua
ua = UserAgent(path='tools/ua.json')
# redis_cli = redis.Redis(decode_responses=True)
# filename = [i for i in os.listdir('woff_file') if '.json' in i]
# print(filename)
#
# with open('woff_file/' + 'b2b8083a.json' ,'r',encoding='utf-8') as f:
#     data = f.read()
# print(data)
# print(type(data))
# print(json.loads(data))
import random
import uuid
from time import time

sjson_1 = {'&#xe116;': '1', '&#xede7;': '2', '&#xe0fb;': '3', '&#xf75c;': '4', '&#xe441;': '5', '&#xf185;': '6', '&#xf522;': '7', '&#xf75d;': '8', '&#xf1e4;': '9', '&#xf82c;': '0', '&#xe8b3;': '店', '&#xf172;': '中', '&#xe68b;': '美', '&#xf036;': '家', '&#xee64;': '馆', '&#xf420;': '小', '&#xf6bc;': '车', '&#xf32b;': '大', '&#xf7ac;': '市', '&#xe6da;': '公', '&#xe0aa;': '酒', '&#xea7b;': '行', '&#xf6b4;': '国', '&#xed09;': '品', '&#xe9ff;': '发', '&#xeae7;': '电', '&#xf091;': '金', '&#xe9f8;': '心', '&#xe24f;': '业', '&#xf381;': '商', '&#xe53b;': '司', '&#xf61d;': '超', '&#xe77e;': '生', '&#xe34c;': '装', '&#xe668;': '园', '&#xee16;': '场', '&#xf2ee;': '食', '&#xe251;': '有', '&#xf321;': '新', '&#xf507;': '限', '&#xf1fd;': '天', '&#xe0b6;': '面', '&#xeab3;': '工', '&#xeaee;': '服', '&#xea91;': '海', '&#xec47;': '华', '&#xee44;': '水', '&#xe2e7;': '房', '&#xf664;': '饰', '&#xf038;': '城', '&#xe819;': '乐', '&#xe37b;': '汽', '&#xece5;': '香', '&#xf5b8;': '部', '&#xe163;': '利', '&#xe4a1;': '子', '&#xed21;': '老', '&#xe10d;': '艺', '&#xe430;': '花', '&#xf23d;': '专', '&#xf811;': '东', '&#xe623;': '肉', '&#xe703;': '菜', '&#xef03;': '学', '&#xef24;': '福', '&#xed2d;': '饭', '&#xf656;': '人', '&#xe5d4;': '百', '&#xeccc;': '餐', '&#xe022;': '茶', '&#xeea2;': '务', '&#xef10;': '通', '&#xf7df;': '味', '&#xe02c;': '所', '&#xe6fc;': '山', '&#xee9b;': '区', '&#xe3da;': '门', '&#xe9e8;': '药', '&#xf19d;': '银', '&#xef21;': '农', '&#xe69e;': '龙', '&#xe824;': '停', '&#xed9b;': '尚', '&#xefb5;': '安', '&#xf6df;': '广', '&#xefaf;': '鑫', '&#xe907;': '一', '&#xf27a;': '容', '&#xe70b;': '动', '&#xeed1;': '南', '&#xf614;': '具', '&#xe229;': '源', '&#xeb99;': '兴', '&#xe8c5;': '鲜', '&#xe789;': '记', '&#xe025;': '时', '&#xe76a;': '机', '&#xf8a3;': '烤', '&#xf7b4;': '文', '&#xe995;': '康', '&#xef7d;': '信', '&#xf1e8;': '果', '&#xf667;': '阳', '&#xedcf;': '理', '&#xe26a;': '锅', '&#xefa3;': '宝', '&#xf73a;': '达', '&#xf7c3;': '地', '&#xf5e1;': '儿', '&#xe478;': '衣', '&#xe0de;': '特', '&#xea06;': '产', '&#xf5d3;': '西', '&#xebad;': '批', '&#xe4fa;': '坊', '&#xe1b0;': '州', '&#xe4eb;': '牛', '&#xf405;': '佳', '&#xec20;': '化', '&#xf002;': '五', '&#xe0e5;': '米', '&#xe2f5;': '修', '&#xf836;': '爱', '&#xf556;': '北', '&#xf6b2;': '养', '&#xf156;': '卖', '&#xf7ff;': '建', '&#xe30f;': '材', '&#xe984;': '三', '&#xe160;': '会', '&#xe3e8;': '鸡', '&#xe63a;': '室', '&#xf41f;': '红', '&#xf7a8;': '站', '&#xf459;': '德', '&#xebba;': '王', '&#xf53b;': '光', '&#xf6e8;': '名', '&#xf8dc;': '丽', '&#xf5c0;': '油', '&#xedf0;': '院', '&#xe953;': '堂', '&#xf160;': '烧', '&#xec16;': '江', '&#xf82f;': '社', '&#xe01e;': '合', '&#xf86d;': '星', '&#xeb90;': '货', '&#xf0ac;': '型', '&#xe2fa;': '村', '&#xf56a;': '自', '&#xec36;': '科', '&#xee79;': '快', '&#xec8a;': '便', '&#xf542;': '日', '&#xe1d0;': '民', '&#xe642;': '营', '&#xf47c;': '和', '&#xf6f0;': '活', '&#xf080;': '童', '&#xed9d;': '明', '&#xee55;': '器', '&#xf14f;': '烟', '&#xf5ec;': '育', '&#xea10;': '宾', '&#xec46;': '精', '&#xe4f4;': '屋', '&#xed6f;': '经', '&#xf8db;': '居', '&#xf57e;': '庄', '&#xe5f0;': '石', '&#xec4e;': '顺', '&#xecc5;': '林', '&#xf883;': '尔', '&#xf606;': '县', '&#xeae6;': '手', '&#xe209;': '厅', '&#xef8f;': '销', '&#xea2b;': '用', '&#xf77c;': '好', '&#xeb3d;': '客', '&#xea3f;': '火', '&#xf0d4;': '雅', '&#xe708;': '盛', '&#xe504;': '体', '&#xec54;': '旅', '&#xf77d;': '之', '&#xf8f0;': '鞋', '&#xe761;': '辣', '&#xf5c5;': '作', '&#xf137;': '粉', '&#xeaec;': '包', '&#xf09c;': '楼', '&#xe22b;': '校', '&#xf824;': '鱼', '&#xeb94;': '平', '&#xee47;': '彩', '&#xf092;': '上', '&#xf22b;': '吧', '&#xefbd;': '保', '&#xe13e;': '永', '&#xe669;': '万', '&#xf6b7;': '物', '&#xeba9;': '教', '&#xe76f;': '吃', '&#xe749;': '设', '&#xf762;': '医', '&#xe3d8;': '正', '&#xef48;': '造', '&#xf688;': '丰', '&#xef92;': '健', '&#xe71a;': '点', '&#xf752;': '汤', '&#xefbf;': '网', '&#xf726;': '庆', '&#xe293;': '技', '&#xf691;': '斯', '&#xe360;': '洗', '&#xe07f;': '料', '&#xe202;': '配', '&#xf2fd;': '汇', '&#xebb9;': '木', '&#xe037;': '缘', '&#xe6c7;': '加', '&#xe76e;': '麻', '&#xf175;': '联', '&#xe6dc;': '卫', '&#xf6f8;': '川', '&#xf6a2;': '泰', '&#xeea3;': '色', '&#xeecd;': '世', '&#xecb3;': '方', '&#xf410;': '寓', '&#xf8ca;': '风', '&#xefd6;': '幼', '&#xf603;': '羊', '&#xf351;': '烫', '&#xe706;': '来', '&#xe9b5;': '高', '&#xf144;': '厂', '&#xf538;': '兰', '&#xe2ad;': '阿', '&#xe5bd;': '贝', '&#xeb6d;': '皮', '&#xe43e;': '全', '&#xe4fe;': '女', '&#xe7b5;': '拉', '&#xf1fc;': '成', '&#xf641;': '云', '&#xf0f8;': '维', '&#xe109;': '贸', '&#xf5dd;': '道', '&#xe8f6;': '术', '&#xe79e;': '运', '&#xe32a;': '都', '&#xe489;': '口', '&#xe78a;': '博', '&#xedf2;': '河', '&#xe46b;': '瑞', '&#xefdf;': '宏', '&#xf11a;': '京', '&#xf18c;': '际', '&#xe5b7;': '路', '&#xe110;': '祥', '&#xe60d;': '青', '&#xe47e;': '镇', '&#xeee2;': '厨', '&#xe576;': '培', '&#xf81d;': '力', '&#xf081;': '惠', '&#xeeca;': '连', '&#xee41;': '马', '&#xe915;': '鸿', '&#xe4a4;': '钢', '&#xf694;': '训', '&#xf7a3;': '影', '&#xec62;': '甲', '&#xe16b;': '助', '&#xf74e;': '窗', '&#xeb21;': '布', '&#xeba4;': '富', '&#xe686;': '牌', '&#xe019;': '头', '&#xe195;': '四', '&#xe24e;': '多', '&#xe2f1;': '妆', '&#xf0d2;': '吉', '&#xe224;': '苑', '&#xf3cd;': '沙', '&#xf31b;': '恒', '&#xf8d2;': '隆', '&#xedec;': '春', '&#xf770;': '干', '&#xf383;': '饼', '&#xe773;': '氏', '&#xe654;': '里', '&#xe0e1;': '二', '&#xe796;': '管', '&#xe34b;': '诚', '&#xf3fd;': '制', '&#xe676;': '售', '&#xf533;': '嘉', '&#xe76d;': '长', '&#xf6d6;': '轩', '&#xefbe;': '杂', '&#xecba;': '副', '&#xee5e;': '清', '&#xf611;': '计', '&#xe083;': '黄', '&#xf3ce;': '讯', '&#xf0ed;': '太', '&#xe2c2;': '鸭', '&#xe570;': '号', '&#xe9c7;': '街', '&#xe0c6;': '交', '&#xe105;': '与', '&#xee6d;': '叉', '&#xe3d6;': '附', '&#xe97c;': '近', '&#xe61c;': '层', '&#xe74c;': '旁', '&#xe20d;': '对', '&#xea98;': '巷', '&#xe37a;': '栋', '&#xe885;': '环', '&#xe78e;': '省', '&#xe9ad;': '桥', '&#xeefc;': '湖', '&#xf841;': '段', '&#xe6b6;': '乡', '&#xe712;': '厦', '&#xf494;': '府', '&#xe541;': '铺', '&#xe858;': '内', '&#xe80a;': '侧', '&#xf0ba;': '元', '&#xf7e0;': '购', '&#xe7f8;': '前', '&#xf820;': '幢', '&#xe756;': '滨', '&#xf13f;': '处', '&#xe1c3;': '向', '&#xe786;': '座', '&#xee1d;': '下', '&#xee3b;': '県', '&#xe566;': '凤', '&#xe5a5;': '港', '&#xf7fe;': '开', '&#xf011;': '关', '&#xf87d;': '景', '&#xf126;': '泉', '&#xe2f4;': '塘', '&#xf1f1;': '放', '&#xf315;': '昌', '&#xf2b6;': '线', '&#xebc7;': '湾', '&#xe249;': '政', '&#xefbb;': '步', '&#xedfb;': '宁', '&#xeba3;': '解', '&#xf885;': '白', '&#xee7d;': '田', '&#xea27;': '町', '&#xe641;': '溪', '&#xece3;': '十', '&#xf4ca;': '八', '&#xe1bb;': '古', '&#xf4a0;': '双', '&#xf813;': '胜', '&#xed81;': '本', '&#xe064;': '单', '&#xf181;': '同', '&#xf4cd;': '九', '&#xf783;': '迎', '&#xe1a4;': '第', '&#xe17a;': '台', '&#xeecf;': '玉', '&#xf3ba;': '锦', '&#xe4c0;': '底', '&#xf11c;': '后', '&#xeb0d;': '七', '&#xe505;': '斜', '&#xe888;': '期', '&#xe964;': '武', '&#xe864;': '岭', '&#xe207;': '松', '&#xe1d3;': '角', '&#xf560;': '纪', '&#xea51;': '朝', '&#xe3ae;': '峰', '&#xf5e7;': '六', '&#xeec1;': '振', '&#xf1b3;': '珠', '&#xe1a1;': '局', '&#xf4c0;': '岗', '&#xe247;': '洲', '&#xf6fb;': '横', '&#xe900;': '边', '&#xe7df;': '济', '&#xecaf;': '井', '&#xe3e1;': '办', '&#xedaf;': '汉', '&#xf5ca;': '代', '&#xe93c;': '临', '&#xec0f;': '弄', '&#xf076;': '团', '&#xec08;': '外', '&#xe7c3;': '塔', '&#xe7b1;': '杨', '&#xf535;': '铁', '&#xeed6;': '浦', '&#xee8e;': '字', '&#xe52f;': '年', '&#xe463;': '岛', '&#xed7d;': '陵', '&#xe205;': '原', '&#xf7e7;': '梅', '&#xe5d0;': '进', '&#xe592;': '荣', '&#xf600;': '友', '&#xea47;': '虹', '&#xf46f;': '央', '&#xe268;': '桂', '&#xf47a;': '沿', '&#xf58f;': '事', '&#xe726;': '津', '&#xe57d;': '凯', '&#xe4a3;': '莲', '&#xe57c;': '丁', '&#xe194;': '秀', '&#xe356;': '柳', '&#xe54c;': '集', '&#xefe5;': '紫', '&#xed59;': '旗', '&#xece7;': '张', '&#xebe1;': '谷', '&#xe8af;': '的', '&#xf327;': '是', '&#xf06d;': '不', '&#xf4ff;': '了', '&#xe8b4;': '很', '&#xe7b3;': '还', '&#xef5b;': '个', '&#xf1c2;': '也', '&#xeba6;': '这', '&#xe03b;': '我', '&#xe38e;': '就', '&#xe844;': '在', '&#xea9f;': '以', '&#xeb73;': '可', '&#xf346;': '到', '&#xe3e2;': '错', '&#xe342;': '没', '&#xe8a0;': '去', '&#xf157;': '过', '&#xe2ec;': '感', '&#xe266;': '次', '&#xe5bb;': '要', '&#xe57e;': '比', '&#xf00e;': '觉', '&#xe71c;': '看', '&#xf68a;': '得', '&#xf127;': '说', '&#xf025;': '常', '&#xe69a;': '真', '&#xe203;': '们', '&#xe370;': '但', '&#xee81;': '最', '&#xe993;': '喜', '&#xe1c6;': '哈', '&#xe9eb;': '么', '&#xe569;': '别', '&#xec1f;': '位', '&#xf2ca;': '能', '&#xe0a9;': '较', '&#xf77f;': '境', '&#xf7d6;': '非', '&#xf416;': '为', '&#xe70f;': '欢', '&#xe5d2;': '然', '&#xf3e7;': '他', '&#xecf0;': '挺', '&#xe6d8;': '着', '&#xe0ab;': '价', '&#xf714;': '那', '&#xe20c;': '意', '&#xf16a;': '种', '&#xe0ac;': '想', '&#xe006;': '出', '&#xeea6;': '员', '&#xe2fc;': '两', '&#xef61;': '推', '&#xecb7;': '做', '&#xee83;': '排', '&#xe21f;': '实', '&#xeaf1;': '分', '&#xe3e9;': '间', '&#xeca5;': '甜', '&#xf5d1;': '度', '&#xeaf8;': '起', '&#xf2c2;': '满', '&#xf676;': '给', '&#xedfe;': '热', '&#xea75;': '完', '&#xe92c;': '格', '&#xe1c2;': '荐', '&#xf655;': '喝', '&#xede1;': '等', '&#xe849;': '其', '&#xe8bf;': '再', '&#xe288;': '几', '&#xe007;': '只', '&#xf8cc;': '现', '&#xec7e;': '朋', '&#xec29;': '候', '&#xe51f;': '样', '&#xe405;': '直', '&#xea21;': '而', '&#xe693;': '买', '&#xe419;': '于', '&#xeb9c;': '般', '&#xf30f;': '豆', '&#xf019;': '量', '&#xe0f3;': '选', '&#xe527;': '奶', '&#xe6f0;': '打', '&#xf0b7;': '每', '&#xf22a;': '评', '&#xe83b;': '少', '&#xf3aa;': '算', '&#xe594;': '又', '&#xe7ea;': '因', '&#xeb7a;': '情', '&#xe4ac;': '找', '&#xeee3;': '些', '&#xebd2;': '份', '&#xee00;': '置', '&#xe328;': '适', '&#xf2ed;': '什', '&#xe2bd;': '蛋', '&#xf79d;': '师', '&#xefe6;': '气', '&#xf645;': '你', '&#xe8ae;': '姐', '&#xeae5;': '棒', '&#xec9f;': '试', '&#xf6d5;': '总', '&#xe825;': '定', '&#xeb22;': '啊', '&#xeeac;': '足', '&#xf121;': '级', '&#xf761;': '整', '&#xf838;': '带', '&#xee28;': '虾', '&#xe5d9;': '如', '&#xe22c;': '态', '&#xef9e;': '且', '&#xf44a;': '尝', '&#xed53;': '主', '&#xf5cb;': '话', '&#xf75a;': '强', '&#xe148;': '当', '&#xf018;': '更', '&#xe9e0;': '板', '&#xf8d1;': '知', '&#xedcc;': '己', '&#xec01;': '无', '&#xe68f;': '酸', '&#xec30;': '让', '&#xf108;': '入', '&#xf4c6;': '啦', '&#xf8bc;': '式', '&#xe6c0;': '笑', '&#xe9a6;': '赞', '&#xec14;': '片', '&#xe420;': '酱', '&#xe9f3;': '差', '&#xf725;': '像', '&#xec88;': '提', '&#xeae2;': '队', '&#xf28f;': '走', '&#xea89;': '嫩', '&#xe1f1;': '才', '&#xec5f;': '刚', '&#xe2dd;': '午', '&#xe457;': '接', '&#xf894;': '重', '&#xea95;': '串', '&#xe26b;': '回', '&#xe7c1;': '晚', '&#xe3e6;': '微', '&#xedcd;': '周', '&#xf396;': '值', '&#xeda4;': '费', '&#xe1eb;': '性', '&#xf2dc;': '桌', '&#xf2d0;': '拍', '&#xe06f;': '跟', '&#xf194;': '块', '&#xe8b7;': '调', '&#xf830;': '糕'}

with open('1.json','w',encoding='utf-8') as f:
    f.write(json.dumps(sjson_1))

'Math.floor(65536 * (1 + Math.random())).toString(16).substring(1)'

print(random.random())

# n = int(65536 * (1 + random.random()))
# print(n)
# print(int(n))
# s = hex(int(n))
# print(s.replace('0x',''))

def enpytro():
    s = hex(int(65536 * (1 + random.random())))
    return s.replace('0x','')[1:]

def get_hc_v():
    return enpytro() + enpytro() + "-" + enpytro() + "-" + enpytro() + "-" + enpytro() + "-" + enpytro() + enpytro() + enpytro() + '.' + str(int(time()))


# comment = {'user_name': '阳光365家具', 'user_level': 'lv1', 'user_vip': 0, 'shopname': '阳光365办公家具(龙华店)', 'shop_score': 50.0, 'pro_score': '产品：5.0', 'env_score': '5.0', 'ser_score': '5.0', 'comment': '深圳市龙华新区和平东路清湖地铁口阳光365国际家具广场办公家具民用家具', 'com_date': '2014-01-17 16:45', 'url': 'http://www.dianping.com/shop/l2oIht3PEa2N4chc/review_all', 'create_time': '2020-06-05 08:07:35', 'shopid': 'l2oIht3PEa2N4chc', 'id': 'd1ac7f653e4d15200029d8716e6773c1'}
# comment = {'user_name': '萍儿._1983', 'user_level': 'lv1', 'user_vip': 0, 'shopname': '雅兰床垫(布吉大芬店)', 'shop_score': 50.0, 'pro_score': '', 'env_score': '', 'ser_score': '', 'comment': '多家对比还是觉得雅兰老品牌，质量很好，睡得安心，用的放心，可以让家人有个好的睡眠是至关重要，身体健康要有好的睡眠，所以一张好的床垫很重要，店员也服务热情，产品讲解很透澈。', 'com_date': '2020-01-02 14:01', 'url': 'http://www.dianping.com/shop/k7vJnN5aWHtFKXGq/review_all', 'create_time': '2020-06-05 16:23:08', 'shopid': 'k7vJnN5aWHtFKXGq', 'id': 'd7ced967794cadf35f236e6528cfcc1b'}
# conn = psycopg2.connect(database="mt_wm_test", user="postgres", password="postgres", host="localhost", port="8635")
# cur = conn.cursor()

# sql = """
#             insert into dianping_comment values ('%(id)s','%(shopid)s','%(shopname)s','%(comment)s','%(url)s','%(user_name)s','%(user_level)s','%(user_vip)s','%(pro_score)s',
#             '%(env_score)s','%(ser_score)s','%(com_date)s','%(create_time)s','%(shop_score)s')
#             """ % comment
# #
# print(sql)
data = {
'cityId': '7',
'cityEnName': 'shenzhen',
'promoId': '0',
'shopType': '10',
'categoryId': '3017',
'regionId': '',
'sortMode': '2',
'shopSortItem': '',
'searchType': '1',
'branchGroupId': '0',
'aroundShopId': '0',
'shippingTypeFilterValue': '0',
'page': '1',
# 'glong1': '113.9645130316162',
# 'glat1': '22.54462384940838',
'glong2': '113.976829',
'glat2': '22.527975'
}
headers = {
        'Accept': 'application/json, text/javascript',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8;',
        'Host': 'www.dianping.com',
        'Origin': 'http://www.dianping.com',
        'Referer': 'http://www.dianping.com/search/map/category/7/20/g112',
        'User-Agent': ua.random,
        # 'Cookie': 's_ViewType=10; _lxsdk_cuid=17263a5f11cc8-0a35404038c5e8-f7d1d38-1fa400-17263a5f11c6f',
            'Cookie':"_hc.v={};s_ViewType=10;".format(get_hc_v()),
        'X-Request': 'JSON',
        'X-Requested-With': 'XMLHttpRequest',
        }

resp = requests.post(url='http://www.dianping.com/search/map/ajax/json',headers=headers,data=data)
print(resp.content.decode())