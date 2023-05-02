# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#spider運作的流程

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 可以對資料再進行處理，在本例中可以進行貨幣單位轉換、擷取資料中的特定部分、或是將資料存入DB等等
class Spider1Pipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        # strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            # 除了description的資料都迭代一遍
            if field_name != 'description':
                #使用dict的get拿到value
                value = adapter.get(field_name)
                #把value的空格拿掉後放回原處
                adapter[field_name] = value[0].strip()

        # Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
    

        # Price --> convert to float
        # price_keys = ['price', 'peice_excl_tax', 'price_incl_tax', 'tax']
        # for price_key in price_keys:
        #     value = adapter.get(price_key)
        #     value = value.replace('£', '')
        #     adapter['price_key'] = float(value)


        # Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        # 其中一筆資料為例: 'In stock (18 available)'
        split_string_array = availability_string.split('(')
        # 若無庫存則不會有(表示len為1
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            # list為['In stock', '18 available']
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])


        # Reviews --> convert to int
        num_review_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_review_string)


        # Stars --> convert to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        print(stars_string)
        print('**********')
        print(split_stars_array)
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == 'zero':
            adapter['stars'] == 0
        elif stars_text_value == 'one':
            adapter['stars'] == 1
        elif stars_text_value == 'two':
            adapter['stars'] == 2
        elif stars_text_value == 'three':
            adapter['stars'] == 3
        elif stars_text_value == 'four':
            adapter['stars'] == 4
        elif stars_text_value == 'five':
            adapter['stars'] == 5


        return item
