# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
import psycopg2


# write result to csv file
class StatsFilePipeline:
    def __init__(self):
        self.dir = os.getcwd()
        print("working directory", self.dir)
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

# class StatsPostgresPipeline:
#     def __init__(self):
#         self.conn = psycopg2.connect('postgres:///vonng')
#
#
#     def process_item(self, item, spider):
#         #   1   2    3     4       5      6     7     8     9
#         # name,code,ur_code,rank,parent,province,city,county,town,village
#         data = (item.get("name", ""),
#                 item.get("code", ""),
#                 item.get("code2", ""),
#                 item.get("rank", ""),
#                 item.get("parent", ""),
#                 item.get("province", ""),
#                 item.get("city", ""),
#                 item.get("county", ""),
#                 item.get("town", ""),
#                 item.get("village", ""))
#
#         with self.conn.cursor() as cur:
#             cur.execute("INSERT INTO ")
#
