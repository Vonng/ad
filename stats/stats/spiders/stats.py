import scrapy
from scrapy import Request
from ..items import *
import re
from urllib.parse import urljoin

ProvinceMap = {"北京市": "110000000000", "天津市": "120000000000", "河北省": "130000000000", "山西省": "140000000000",
               "内蒙古自治区": "150000000000", "辽宁省": "210000000000", "吉林省": "220000000000", "黑龙江省": "230000000000",
               "上海市": "310000000000", "江苏省": "320000000000", "浙江省": "330000000000", "安徽省": "340000000000",
               "福建省": "350000000000", "江西省": "360000000000", "山东省": "370000000000", "河南省": "410000000000",
               "湖北省": "420000000000", "湖南省": "430000000000", "广东省": "440000000000", "广西壮族自治区": "450000000000",
               "海南省": "460000000000", "重庆市": "500000000000", "四川省": "510000000000", "贵州省": "520000000000",
               "云南省": "530000000000", "西藏自治区": "540000000000", "陕西省": "610000000000", "甘肃省": "620000000000",
               "青海省": "630000000000", "宁夏回族自治区": "640000000000", "新疆维吾尔自治区": "650000000000", "台湾省": "710000000000",
               "香港特别行政区": "810000000000", "澳门特别行政区": "820000000000"}


class StatsSpider(scrapy.Spider):
    name = 'stats'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/']

    def __init__(self, year='2020', *args, **kwargs):
        super(StatsSpider, self).__init__(*args, **kwargs)
        self.year = year
        self.baseurl = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/%s/' % self.year

        # 解析入口

    def parse(self, response, **kwargs):
        # 产出固定记录：中国，港、澳、台
        china, taiwan, hongkong, macao = ProvinceItem(), ProvinceItem(), ProvinceItem(), ProvinceItem()
        china["name"], china["code"], china["rank"], china["parent"] = "中华人民共和国", "100000000000", 0, "100000000000"
        taiwan["name"], taiwan["code"], taiwan["rank"], taiwan["parent"] = "台湾省", "710000000000", 1, "100000000000"
        hongkong["name"], hongkong["code"], hongkong["rank"], hongkong[
            "parent"] = "香港特别行政区", "810000000000", 1, "100000000000"
        macao["name"], macao["code"], macao["rank"], macao["parent"] = "澳门特别行政区", "820000000000", 1, "100000000000"
        yield china
        yield taiwan
        yield hongkong
        yield macao

        start_url = urljoin(self.baseurl, 'index.html')
        yield Request(start_url, callback=self.parse_country, meta={
            "parent": "100000000000",  # 省份的上级是国家，虚拟代码：100000000000
        })  # 生成首页爬取请求

    # 处理首页
    def parse_country(self, response):
        for node in response.xpath('//tr[@class="provincetr"]/td'):
            name = node.xpath('./a/text()').get()  # 省份名称
            if not name or name == '': continue
            code = ProvinceMap[name]  # 省份代码
            link = node.xpath('./a/@href').get()

            item = ProvinceItem()
            item['name'], item['code'], item['rank'], item['parent'] = name, code, 1, "100000000000"
            item['province'] = name
            yield item  # 产出省份

            if link:  # 生成省份请求
                url = urljoin(response.request.url, link)
                yield Request(url, callback=self.parse_province, meta={
                    "parent": code,  # 省份的上级是国家，虚拟代码：100000000000
                    "province": name,
                })

    # 处理省份详情页面，每个元素是一个城市
    def parse_province(self, response):
        province = response.meta["province"]

        for node in response.xpath('//tr[@class="citytr"]'):
            name = node.xpath('./td[2]/a/text()').get()
            if not name or name == '': continue
            code = node.xpath('./td[1]/a/text()').get()
            link = node.xpath('./td[2]/a/@href').get()

            item = CityItem()
            item['name'], item['code'], item['rank'], item['parent'] = name, code, 2, response.meta["parent"]
            item['province'], item['city'] = province, name
            yield item

            if link:  # 生成城市请求
                url = urljoin(response.request.url, link)
                yield Request(url, callback=self.parse_city, meta={
                    "parent": code,
                    "province": province,
                    "city": name
                })

    # 处理城市详情页面，每个元素是一个区县
    def parse_city(self, response):
        province, city = response.meta["province"], response.meta["city"]

        # 城市页面有些特殊，可能包含一个不带链接的"市辖区"
        for node in response.xpath('//tr[@class="countytr"]'):
            name = node.xpath('./td[2]').xpath('string(.)').get()
            if not name or name == '': continue
            code = node.xpath('./td[1]').xpath('string(.)').get()
            link = node.xpath('./td[2]/a/@href').get()

            item = CountyItem()
            item['name'], item['code'], item['rank'], item['parent'] = name, code, 3, response.meta["parent"]
            item['province'], item['city'], item['county'] = province, city, name
            yield item

            if link:  # 生成区县请求
                # /tjsj/tjbz/tjyqhdmhcxhfdm/2020/35.html --[35/3504.html]-> /tjsj/tjbz/tjyqhdmhcxhfdm/2020/35/3504.html
                url = urljoin(response.request.url, link)
                yield Request(url, callback=self.parse_county, meta={
                    "parent": code,
                    "province": province,
                    "city": city,
                    "county": name
                })

    # 处理区县详情页面，每个元素是一个乡镇
    def parse_county(self, response):
        province, city, county = response.meta["province"], response.meta["city"], response.meta["county"]
        for node in response.xpath('//tr[@class="towntr"]'):
            name = node.xpath('./td[2]/a/text()').get()
            if not name or name == '': continue
            code = node.xpath('./td[1]/a/text()').get()
            link = node.xpath('./td[2]/a/@href').get()

            item = VillageItem()
            item['name'], item['code'], item['rank'], item['parent'] = name, code, 4, response.meta["parent"]
            item['province'], item['city'], item['county'], item['town'] = province, city, county, name
            yield item

            # /tjsj/tjbz/tjyqhdmhcxhfdm/2019/54/06/540630.html ---- [30/540630205.html]
            # /tjsj/tjbz/tjyqhdmhcxhfdm/2019/54/06/30/540630205.html
            if link:  # 生成乡镇请求
                url = urljoin(response.request.url, link)
                yield Request(url, callback=self.parse_town, meta={
                    "parent": code,
                    "province": province,
                    "city": city,
                    "county": county,
                    "town": name
                })

    # 处理乡镇详情页面，每个元素是一个村/居委会
    def parse_town(self, response):
        province, city, county, town = response.meta["province"], response.meta["city"], response.meta["county"], \
                                       response.meta["town"]
        for node in response.xpath('//tr[@class="villagetr"]'):
            name = node.xpath('./td[3]/text()').get()
            if not name or name == '': continue
            code = node.xpath('./td[1]/text()').get()
            code2 = node.xpath('./td[2]/text()').get()  # 城乡统计代码

            item = VillageItem()
            item['name'], item['code'], item['rank'], item['parent'] = name, code, 5, response.meta["parent"]
            item['province'], item['city'], item['county'], item['town'], item[
                "village"] = province, city, county, town, name
            item['code2'] = code2
            yield item
