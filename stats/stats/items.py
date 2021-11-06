# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


# 1级行政区划：省
class ProvinceItem(scrapy.Item):
    name = Field()
    code = Field()
    rank = Field()
    parent = Field()
    province = Field()
    city = Field()
    county = Field()
    town = Field()
    village = Field()


# 2级行政区划：市
class CityItem(scrapy.Item):
    name = Field()
    code = Field()
    rank = Field()
    parent = Field()
    province = Field()
    city = Field()
    county = Field()
    town = Field()
    village = Field()

# 3级行政区划：区/县
class CountyItem(scrapy.Item):
    name = Field()
    code = Field()
    rank = Field()
    parent = Field()
    province = Field()
    city = Field()
    county = Field()
    town = Field()
    village = Field()


# 4级行政区划：乡/镇/街道
class TownItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    rank = Field()
    parent = Field()
    province = Field()
    city = Field()
    county = Field()
    town = Field()
    village = Field()


# 4级行政区划：村/居委会
class VillageItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    rank = Field()
    parent = Field()
    province = Field()
    city = Field()
    county = Field()
    town = Field()
    village = Field()
    code2 = scrapy.Field()  # 城乡统计代码
