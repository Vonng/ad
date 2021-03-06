# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os


# write result to csv file
class NbsFilePipeline:
    def __init__(self):
        self.dir = os.getcwd()
        print("working directory", self.dir)
        try:
            os.mkdir(os.path.join(self.dir, 'data'))
        except:
            pass
        self.f = None  # open('/tmp/data.csv', 'w')

    def process_item(self, item, spider):
        year = spider.year
        if self.f is None:
            self.fpath = os.path.join(self.dir, 'data', '%s.csv' % year)
            self.f = open(self.fpath, 'w')

        #   1   2    3     4       5      6     7     8     9
        # name,code,ur_code,rank,parent,province,city,county,town,village
        result = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
            item.get("code", ""),
            item.get("parent", ""),
            item.get("code2", ""),
            item.get("rank", ""),
            item.get("name", ""),
            item.get("province", ""),
            item.get("city", ""),
            item.get("county", ""),
            item.get("town", ""),
            item.get("village", "")
        )
        self.f.write(result)
        self.f.flush()
        return item


import psycopg2


# write result to postgres database
class NbsPsqlPipeline:
    def __init__(self):
        self.conn = None

    def process_item(self, item, spider):
        year = spider.year
        pgurl = spider.pgurl
        table_name = 'ad.nbs_%s' % year
        if self.conn is None:
            self.conn = psycopg2.connect(pgurl)

        sql = "INSERT INTO " + table_name + " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;"
        data = (
            item.get("code", ""),
            item.get("parent", ""),
            item.get("code2", None),
            item.get("rank", None),
            item.get("name", None),
            item.get("province", None),
            item.get("city", None),
            item.get("county", None),
            item.get("town", None),
            item.get("village", None)
        )

        with self.conn.cursor() as cur:
            cur.execute(sql, data)
        self.conn.commit()
        return item
