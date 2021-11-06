# 国家统计局行政区划代码（爬虫）

## 使用方式

爬取2020年行政区划代码，可以使用以下命令：

```bash
nohup scrapy crawl stats -a year=2020 --logfile=2020.log &
```

输出数据格式

```sql
CREATE TABLE ad.stats
(
    code     BIGINT      NOT NULL,
    parent   BIGINT      NOT NULL,
    urcode   SMALLINT,
    rank     SMALLINT    NOT NULL CHECK (rank >= 0 AND rank <= 5),
    name     VARCHAR(64) NOT NULL,
    province varchar(64),
    city     varchar(64),
    county   varchar(64),
    town     varchar(64),
    village  varchar(64)
);
```

```csv
433130005000,433130000000,,4,石羔街道,湖南省,湘西土家族苗族自治州,龙山县,石羔街道,
433130104000,433130000000,,4,洗车河镇,湖南省,湘西土家族苗族自治州,龙山县,洗车河镇,
433130110000,433130000000,,4,石牌镇,湖南省,湘西土家族苗族自治州,龙山县,石牌镇,
```