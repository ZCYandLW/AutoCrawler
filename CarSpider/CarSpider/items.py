# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarCommentItem(scrapy.Item):
    # 口碑item
    desc = scrapy.Field()
    user_name = scrapy.Field()
    publish_time = scrapy.Field()
    buy_time = scrapy.Field()
    car_type = scrapy.Field()
    buy_address = scrapy.Field()
    buy_prices = scrapy.Field()
    run_km = scrapy.Field()
    comment = scrapy.Field()

    def get_insert_sql(self):
        # 返回插入数据库sql语句和对应字段的值的元组
        insert_sql = """insert into car_comment(comment_desc,user_name,publish_time,buy_time,car_type,buy_address,buy_prices,run_km,comment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE buy_address=VALUES(buy_address)
                     ,comment_desc=VALUES(comment_desc)
                     """
        comment_desc = self['desc']
        user_name = self['user_name']
        publish_time = self['publish_time']
        buy_time = self['buy_time']
        car_type = self['car_type']
        buy_address = self['buy_address']
        buy_prices = self['buy_prices']
        run_km = self['run_km']
        comment = self['comment']
        parms = (comment_desc, user_name, publish_time, buy_time, car_type, buy_address, buy_prices, run_km, comment)
        return insert_sql, parms


class CarspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
