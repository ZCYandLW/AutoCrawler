# -*- coding: utf-8 -*-

import re

from urllib import parse
from scrapy.http import Request
import scrapy

from CarSpider.items import CarCommentItem


class CarcommentSpider(scrapy.Spider):
    name = 'carComment'
    allowed_domains = ['k.m.autohome.com.cn/']
    start_urls = ['https://k.m.autohome.com.cn/']
    headers = {

        "User-Agent": "",

    }

    def parse(self, response):
        """
        获取response中a标签的href属性值，符合 .*k.m.autohome.com.cn/(\d+).*的页面就下载并callback到get_comment_detail_url函数处理，不符合
        的就进一步下载，callback回parse函数，继续搜索符合正则表达式的url
        """

        all_urls = response.css('a::attr(href)').extract()  # 获得所有a标签的链接值
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = list(filter(lambda x: True if x.startswith('https') else False, all_urls))  # 过滤不是以https开头的url
        for url in all_urls:
            # 符合正则表达式的url请求并处理细节
            match_obj = re.match("(.*k.m.autohome.com.cn/(\d+)).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                yield Request(request_url, callback=self.get_comment, dont_filter=True, headers=self.headers)
            # else:
            #     yield Request(url, dont_filter=True, headers=self.headers)

    def get_comment(self, response):
        """
        获取每条口碑的购买价格，行驶距离，购买地址，和汽车名字并传递给request的meta
        以及获取每条口碑对应的更加详细的口碑地址并请求该地址后返回pase_detail函数构建口碑的item
        """
        buy_prices = response.xpath('//*[@id="js-koubeilistBox"]/ul/li[2]/span[1]/i/text()').extract()  # 购买价格数组
        run_km_list = response.xpath('//*[@id="js-koubeilistBox"]/ul/li[2]/span[2]/text()').extract()  # 行驶距离数组
        buy_addresses = response.xpath('//*[@id="js-koubeilistBox"]/ul/li[2]/span[3]/text()').extract()  # 购买地址数组
        car_name = response.css('.car-name::text').extract_first()  # 汽车名字
        i = 0  # 数组元素索引值
        urls = response.css('#js-koubeilistBox > ul::attr(onclick)').extract()  # 所有口碑详细内容的地址数组
        for url in urls:
            match_obj = re.match(".*//(.*)'$", url)  # 提取口碑详细内容url
            if match_obj:
                request_url = match_obj.group(1)
                request_url = 'https://' + request_url
                yield Request(request_url, callback=self.pase_detail, dont_filter=True,
                              meta={'buy_price': buy_prices[i], 'car_type': car_name, 'run_km': run_km_list[i],
                                    'buy_address': buy_addresses[i]},
                              headers=self.headers)
            ++i

    def pase_detail(self, response):
        comment_item = CarCommentItem()
        desc = response.css('.wom-details>header>h1::text').extract_first()  # 口碑简短描述
        user_name = response.css('.wom-details>header>div>a>span::text').extract_first()  # 用户名
        publish_time = response.css('.wom-details>header>div>time::text').extract_first()  # 口碑发表时间
        buy_time = response.css('.cartype>span>span::text').extract_first()  # 汽车购买时间
        car_type = response.meta.get('car_type', '')  # 车型
        buy_prices = response.meta.get('buy_price', '')  # 购买价格
        buy_address = response.meta.get('buy_address', '')  # 购买地址
        run_km = response.meta.get('run_km', '')  # 行驶距离
        comment = response.xpath("//*[@class='matter']")
        comment = comment.xpath('string(.)').extract()[0].replace("\n",'').replace(" ",'')  # 取得matter标签下的所有口碑comment并删去换行符和空格
        comment_item['desc'] = desc
        comment_item['user_name'] = user_name
        comment_item['publish_time'] = publish_time
        comment_item['buy_time'] = buy_time
        comment_item['car_type'] = car_type
        comment_item['buy_prices'] = buy_prices
        comment_item['buy_address'] = buy_address
        comment_item['run_km'] = run_km
        comment_item['comment'] = comment
        yield comment_item
