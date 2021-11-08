# 国家统计局行政区划代码（NBS）

National Bureau of Statistics
 

## 爬虫使用方式

爬取2020年行政区划代码，可以使用以下命令：（原始数据包括：2009-202）

```bash
pip3 install scrapy
scrapy crawl nbs     # 不加年份参数时，爬取2020年数据 -a year=2020
```

后台爬取所有数据

```bash
mkdir data log
nohup scrapy crawl nbs -a year=2009 -L INFO --logfile=log/2009.log &
nohup scrapy crawl nbs -a year=2010 -L INFO --logfile=log/2010.log &
nohup scrapy crawl nbs -a year=2011 -L INFO --logfile=log/2011.log &
nohup scrapy crawl nbs -a year=2012 -L INFO --logfile=log/2012.log &
nohup scrapy crawl nbs -a year=2013 -L INFO --logfile=log/2013.log &
nohup scrapy crawl nbs -a year=2014 -L INFO --logfile=log/2014.log &
nohup scrapy crawl nbs -a year=2015 -L INFO --logfile=log/2015.log &
nohup scrapy crawl nbs -a year=2016 -L INFO --logfile=log/2016.log &
nohup scrapy crawl nbs -a year=2017 -L INFO --logfile=log/2017.log &
nohup scrapy crawl nbs -a year=2018 -L INFO --logfile=log/2018.log &
nohup scrapy crawl nbs -a year=2019 -L INFO --logfile=log/2019.log &
nohup scrapy crawl nbs -a year=2020 -L INFO --logfile=log/2020.log &
```

输出数据格式

```sql
-- 国家统计局统计用行政区划代码
CREATE TABLE ad.nbs
(
    code     BIGINT      NOT NULL, -- 12位行政区划代码
    parent   BIGINT      NOT NULL, -- 父级行政区划代码
    urcode   SMALLINT,             -- 城乡性质代码
    rank     SMALLINT    NOT NULL, -- 行政区划等级：0-5 (国省市县乡村)
    name     VARCHAR(64) NOT NULL, -- 行政区划名称
    province VARCHAR(64),          -- 区划所属省份
    city     VARCHAR(64),          -- 区划所属城市
    county   VARCHAR(64),          -- 区划所属区县
    town     VARCHAR(64),          -- 区划所属乡镇街道
    village  VARCHAR(64),          -- 区划所属村/居委会
    PRIMARY KEY (code),            -- 行政区划代码为唯一主键
    CHECK ( rank >= 0 AND rank <= 5 ),
    CHECK ( code >= 100000000000 AND code <= 999999999999 )
);
```

**数据样例**

```csv
100000000000,100000000000,,0,中华人民共和国,,,,,
110000000000,100000000000,,1,北京市,北京市,,,,
110100000000,110000000000,,2,市辖区,北京市,市辖区,,,
110101000000,110100000000,,3,东城区,北京市,市辖区,东城区,,
110101001000,110101000000,,4,东华门街道办事处,北京市,市辖区,东城区,东华门街道办事处,
110101001001,110101001000,111,5,多福巷社区居委会,北京市,市辖区,东城区,东华门街道办事处,多福巷社区居委会
```


**特例说明**

四个筒子市，即不设区县，直接管理乡镇街道的特殊城市：

* 甘肃 [嘉峪关市](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/62/6202.html)
* 广东 [东莞市](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/44/4419.html)
* 广东 [中山市](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/44/4420.html)
* 海南 [儋州市](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/46/4604.html)

其中，广东 东莞市，广东 中山市，海南 儋州市的4级行政区划直接挂载在2级行政区划下。