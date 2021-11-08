import scrapy
from scrapy import Request
from ..items import *
import re
from urllib.parse import urljoin

# return 12 code for provinces
ProvinceMap = {"北京市": "110000000000", "天津市": "120000000000", "河北省": "130000000000", "山西省": "140000000000",
               "内蒙古自治区": "150000000000", "辽宁省": "210000000000", "吉林省": "220000000000", "黑龙江省": "230000000000",
               "上海市": "310000000000", "江苏省": "320000000000", "浙江省": "330000000000", "安徽省": "340000000000",
               "福建省": "350000000000", "江西省": "360000000000", "山东省": "370000000000", "河南省": "410000000000",
               "湖北省": "420000000000", "湖南省": "430000000000", "广东省": "440000000000", "广西壮族自治区": "450000000000",
               "海南省": "460000000000", "重庆市": "500000000000", "四川省": "510000000000", "贵州省": "520000000000",
               "云南省": "530000000000", "西藏自治区": "540000000000", "陕西省": "610000000000", "甘肃省": "620000000000",
               "青海省": "630000000000", "宁夏回族自治区": "640000000000", "新疆维吾尔自治区": "650000000000", "台湾省": "710000000000",
               "香港特别行政区": "810000000000", "澳门特别行政区": "820000000000"}

# 2011, 2012 has different province names
ProvinceAliasMap = {
    "北京": "北京市", "天津": "天津市", "河北": "河北省", "山西": "山西省", "内蒙古": "内蒙古自治区", "辽宁": "辽宁省", "吉林": "吉林省", "黑龙江": "黑龙江省",
    "上海": "上海市", "江苏": "江苏省", "浙江": "浙江省", "安徽": "安徽省", "福建": "福建省", "江西": "江西省", "山东": "山东省", "河南": "河南省", "湖北": "湖北省",
    "湖南": "湖南省", "广东": "广东省", "广西": "广西壮族自治区", "海南": "海南省", "重庆": "重庆市", "四川": "四川省", "贵州": "贵州省", "云南": "云南省",
    "西藏": "西藏自治区", "陕西": "陕西省", "甘肃": "甘肃省", "青海": "青海省", "宁夏": "宁夏回族自治区", "新疆": "新疆维吾尔自治区", "台湾": "台湾省",
    "香港": "香港特别行政区", "澳门": "澳门特别行政区"
}


# return 12 digit code's rank according to code pattern
def code_rank(code):
    code = int(code)
    if code < 100000000000 or code > 999999999999:
        return 9  # invalid rank
    if code == 100000000000: return 0
    if int(code / 10000000000) * 10000000000 == code: return 1
    if int(code / 100000000) * 100000000 == code: return 2
    if int(code / 1000000) * 1000000 == code: return 3
    if int(code / 1000) * 1000 == code:
        return 4
    else:
        return 5


class NbsSpider(scrapy.Spider):
    """爬取国家统计局行政区划代码的爬虫：http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/"""

    name = 'nbs'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/']

    def __init__(self, year='2020', pgurl="", *args, **kwargs):
        """固定参数为年份"""
        super(NbsSpider, self).__init__(*args, **kwargs)
        self.year = year
        self.pgurl = pgurl
        self.baseurl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/%s/' % self.year
        self.filter_enabled = False  # 用于单独处理特例的过滤器，默认关闭
        self.province_filter = ['广东省', '海南省']
        self.city_filter = ['东莞市', '中山市', '儋州市']

    def parse(self, response, **kwargs):
        """入口，生成年份初始页面爬取请求"""
        start_url = urljoin(self.baseurl, 'index.html')
        yield Request(start_url, callback=self.parse_country, meta={
            "parent": "100000000000",  # 省份的上级是国家，虚拟代码：100000000000
        })  # 生成首页爬取请求

    # 处理首页
    def parse_country(self, response):
        """处理年度区划代码首页"""

        base_url = self.short_url(self.baseurl)
        if not self.filter_enabled:
            # 产出固定记录：中国，港、澳、台
            china, taiwan, hongkong, macao = ProvinceItem(), ProvinceItem(), ProvinceItem(), ProvinceItem()
            china["name"], china["code"], china["rank"], china["parent"], china["link"] \
                = "中华人民共和国", "100000000000", 0, "100000000000", base_url
            taiwan["name"], taiwan["code"], taiwan["rank"], taiwan["parent"], taiwan['link'] \
                = "台湾省", "710000000000", 1, "100000000000", base_url
            hongkong["name"], hongkong["code"], hongkong["rank"], hongkong["parent"], hongkong['link'] \
                = "香港特别行政区", "810000000000", 1, "100000000000", base_url
            macao["name"], macao["code"], macao["rank"], macao["parent"], macao['link'] \
                = "澳门特别行政区", "820000000000", 1, "100000000000", base_url
            yield china
            yield taiwan
            yield hongkong
            yield macao

        # 处理其余省份
        for node in response.xpath('//tr[@class="provincetr"]/td'):
            name = node.xpath('./a/text()').get()  # 省份名称
            if not name or name == '': continue
            if self.year == '2011' or self.year == '2012':
                name = ProvinceAliasMap[name]  # 这两年的省份缩写名称不一样，需要映射为标准省份名称
            if self.filter_enabled and name not in self.province_filter: continue

            code = ProvinceMap[name]  # 省份代码
            link = node.xpath('./a/@href').get()
            rank = code_rank(code)
            url = urljoin(response.request.url, link) if link else ""

            if (not name.startswith('台湾') or not name.startswith('香港') or not name.startswith('澳门')):
                item = ProvinceItem()
                item['name'], item['code'], item['rank'], item['parent'], item['link'] \
                    = name, code, rank, "100000000000", base_url
                item['province'] = name
                yield item  # 产出省份

            if url:  # 生成省份页面请求
                if self.filter_enabled and name not in self.province_filter: continue
                yield Request(url, callback=self.get_callback(rank), meta={
                    "parent": code,  # 省份的上级是国家，虚拟代码：100000000000
                    "province": name,
                })

    def parse_province(self, response):
        """处理省份详情页面，每个元素是一个城市"""
        province, parent = response.meta.get("province", ""), response.meta.get("parent", "")

        for node in response.xpath('//tr[@class="citytr"]'):
            name = node.xpath('./td[2]/a/text()').get()
            if not name or name == '': continue
            if self.filter_enabled and name not in self.city_filter: continue

            code = node.xpath('./td[1]/a/text()').get()
            link = node.xpath('./td[2]/a/@href').get()
            rank = code_rank(code)
            url = urljoin(response.request.url, link) if link else ""

            item = CityItem()
            item['name'], item['code'], item['rank'], item['parent'], item['link'] \
                = name, code, rank, parent, self.short_url(response.request.url)
            item['province'], item['city'] = province, name
            yield item

            if link:  # 生成城市请求
                yield Request(url, callback=self.get_callback(rank), meta={
                    "parent": code,
                    "province": province,
                    "city": name
                })

    # 处理城市详情页面，每个元素是一个区县
    def parse_city(self, response):
        province, city, parent \
            = response.meta.get("province", ""), response.meta.get("city", ""), response.meta.get("parent", "")

        # 城市页面有些特殊，可能包含一个不带链接的"市辖区"，以及四个特殊筒子市（不设区，直接管辖乡镇一级）
        for node in response.xpath('//tr[@class="countytr" or @class="towntr"]'):
            name = node.xpath('./td[2]').xpath('string(.)').get()
            if not name or name == '': continue
            code = node.xpath('./td[1]').xpath('string(.)').get()
            link = node.xpath('./td[2]/a/@href').get()
            rank = code_rank(code)
            url = urljoin(response.request.url, link) if link else ""

            item = CountyItem()
            item['name'], item['code'], item['rank'], item['parent'], item['link'] \
                = name, code, rank, parent, self.short_url(response.request.url)
            item['province'], item['city'] = province, city
            if rank == 3:  item['county'] = name
            if rank == 4: item['county'], item["town"] = "", name
            yield item

            if link:  # 生成区县请求
                # /tjsj/tjbz/tjyqhdmhcxhfdm/2020/35.html --[35/3504.html]-> /tjsj/tjbz/tjyqhdmhcxhfdm/2020/35/3504.html
                if rank == 3:  # 普通区县
                    yield Request(url, callback=self.get_callback(rank), meta={
                        "parent": code,
                        "province": province,
                        "city": city,
                        "county": name
                    })
                elif rank == 4:  # 筒子市 直管的区划
                    yield Request(url, callback=self.get_callback(rank), meta={
                        "parent": code,
                        "province": province,
                        "city": city,
                        "county": "",
                        "town": name
                    })

    # 处理区县详情页面，每个元素是一个乡镇
    def parse_county(self, response):
        province, city, county, parent = response.meta.get("province", ''), response.meta.get("city", ''), \
                                         response.meta.get("county"), response.meta.get("parent", "")
        for node in response.xpath('//tr[@class="towntr"]'):
            name = node.xpath('./td[2]/a/text()').get()
            if not name or name == '': continue
            code = node.xpath('./td[1]/a/text()').get()
            link = node.xpath('./td[2]/a/@href').get()
            rank = code_rank(code)
            url = urljoin(response.request.url, link) if link else ""

            item = VillageItem()
            item['name'], item['code'], item['rank'], item['parent'] = name, code, rank, parent
            item['province'], item['city'], item['county'], item['town'], item['link'] \
                = province, city, county, name, self.short_url(response.request.url)
            yield item

            # /tjsj/tjbz/tjyqhdmhcxhfdm/2019/54/06/540630.html ---- [30/540630205.html]
            # /tjsj/tjbz/tjyqhdmhcxhfdm/2019/54/06/30/540630205.html
            if link:  # 生成乡镇请求
                yield Request(url, callback=self.parse_town, meta={
                    "parent": code,
                    "province": province,
                    "city": city,
                    "county": county,
                    "town": name
                })

    # 处理乡镇详情页面，每个元素是一个村/居委会
    def parse_town(self, response):
        province, city, county, town, parent = response.meta.get("province", ''), response.meta.get("city", ''), \
                                               response.meta.get("county", ''), response.meta.get("town", ''), \
                                               response.meta.get("parent", '')
        for node in response.xpath('//tr[@class="villagetr"]'):
            name = node.xpath('./td[3]/text()').get()
            if not name or name == '': continue
            code = node.xpath('./td[1]/text()').get()
            rank = code_rank(code)
            code2 = node.xpath('./td[2]/text()').get()  # 城乡统计代码

            item = VillageItem()
            item['name'], item['code'], item['rank'], item['parent'] = name, code, rank, parent
            item['province'], item['city'], item['county'], item['town'], item["village"], item['link'] \
                = province, city, county, town, name, self.short_url(response.request.url)
            item['code2'] = code2
            yield item

    def get_callback(self, rank):
        """根据行政区划等级，找到恰当的处理函数"""
        if rank == 0:
            return self.parse_country
        elif rank == 1:
            return self.parse_province
        elif rank == 2:
            return self.parse_city
        elif rank == 3:
            return self.parse_county
        elif rank == 4:
            return self.parse_town

    def short_url(self, url):
        if url.startswith('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm'):
            return url[48:]
