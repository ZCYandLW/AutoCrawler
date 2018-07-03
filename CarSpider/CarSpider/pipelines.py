# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class CarspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    """
    使用twisted框架将item内容异步插入数据库
    """

    @classmethod
    def from_settings(cls, settings):
        db_parms = dict(host=settings['MYSQL_HOST'],
                        db=settings['MYSQL_DB_NAME'],
                        user=settings['MYSQL_USER'],
                        passwd=settings['MYSQL_PASSWORD'],
                        charset='utf8',
                        cursorclass=MySQLdb.cursors.DictCursor,
                        use_unicode=True,
                        )
        db_pool = adbapi.ConnectionPool("MySQLdb", **db_parms)
        return cls(db_pool)

    def __init__(self, db_pool):
        self.db_pool = db_pool

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        """
        执行插入
        """
        insert_sql, parms = item.get_insert_sql()
        cursor.execute(insert_sql, parms)

    def handle_error(self, failure, item, spider):
        """
        打印执行插入操作错误信息
        """
        print(failure)
