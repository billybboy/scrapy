# Define here the models for your scraped items
# 最好此用這裡來定義爬蟲下來的項目
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider1Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass


# 若有貨幣符號無法正確顯示時可以使用
def serialize_prize(value):
    return f'£ {str(value)}'


# 以下為新增的class'
# 這麼做的一個原因為在spider yield下打錯字會產生錯誤，若沒有設定item則因為不會產生錯誤而會漏掉錯字
class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
