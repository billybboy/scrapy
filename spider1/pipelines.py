# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#spider運作的流程

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Spider1Pipeline:
    def process_item(self, item, spider):
        return item
