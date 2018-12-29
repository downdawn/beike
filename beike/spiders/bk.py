# -*- coding: utf-8 -*-
import scrapy
from beike.items import BeikeItem
from urllib.parse import urljoin
import re
import json
from copy import deepcopy


class BkSpider(scrapy.Spider):
    name = 'bk'
    allowed_domains = ['bj.zu.ke.com']
    start_urls = ['https://bj.zu.ke.com/zufang/']

    def parse(self, response):
        # print(response.text)
        item = BeikeItem()
        div_list = response.xpath("//div[@class='content__list']/div")
        for div in div_list:
            # item = BeikeItem()
            url_list = div.xpath("./a[@class='content__list--item--aside']/@href").extract()
            # print(url_list)
            for url in url_list:
                item["url"] = "https://bj.zu.ke.com" + url
                print(item["url"])
                result = re.findall(r'http.*?com/(.*?)/.*', item["url"], re.S)
                print(result)
                if result[0] == 'apartment':
                    yield scrapy.Request(
                        item["url"],
                        callback=self.parse_apartment,
                        meta={"item": deepcopy(item)},
                        dont_filter=True
                    )
                elif result[0] == 'zufang':
                    yield scrapy.Request(
                        item["url"],
                        callback=self.parse_zufang,
                        meta={"item": deepcopy(item)},
                        dont_filter=True
                    )

        #列表页翻页
        next_url = response.xpath("//div[@class='content__article']/div[2]/@data-curpage").extract_first()
        max_url = response.xpath("//div[@class='content__article']/div[2]/@data-totalpage").extract_first()
        next_url = int(next_url) + 1
        if int(next_url) <= int(max_url):
            this_url = 'https://bj.zu.ke.com/zufang/pg' + str(next_url)
            print(this_url, '*' * 50)
            item["this_url"] = this_url
            yield scrapy.Request(
                item["this_url"],
                callback=self.parse,
                meta={"item": item}
            )

    def parse_apartment(self, response):
        item = response.meta["item"]
        item["apartment_name"] = response.xpath("//span[@class='aside_neme']/text()").extract_first()
        item["apartment_price"] = response.xpath("//p[@class='content__aside--title']/span[2]/text()").extract_first()
        if item["apartment_price"] is not None:
            item["apartment_price"] = response.xpath(
                "//p[@class='content__aside--title']/span[2]/text()").extract_first().strip()
        item["apartment_mode"] = response.xpath("//p[@class='content__aside--title']/span[2]//span/text()").extract_first()
        item["apartment_master"] = response.xpath("//span[@class='contact_name']/text()").extract_first()
        item["apartment_phone"] = response.xpath("//p[@class='content__aside__list--bottom oneline']/text()").extract_first()
        item["apartment_facility"] = response.xpath("//div[@id='facility']/ul/li/text()").extract()
        item["apartment_renting"] = response.xpath("//div[@id='renting']/ul/li/a/img/@src").extract()
        yield item

    def parse_zufang(self, response):
        item = response.meta["item"]
        item["zufang_name"] = response.xpath("//div[@class='content clear w1150']/p/text()").extract_first()
        item["zufang_time"] = response.xpath("//div[@class='content__subtitle']/text()").extract()[1].strip()[7:]
        item["zufang_house_codes"] = response.xpath("//span[@class='agent__im']/@data-id").extract_first()
        item["zufang_price"] = response.xpath("//p[@class='content__aside--title']/span/text()").extract_first().strip()
        item["zufang_mode"] = response.xpath("//p[@class='content__aside--title']/text()").extract_first()
        item["zufang_tags"] = response.xpath("//p[@class='content__aside--tags']//i/text()").extract()
        item["zufang_article"] = response.xpath("//p[@class='content__article__table']/span/text()").extract()
        # item["zufang_master"] = response.xpath("///div[@id='desc']//div/div/span/text()").extract_first()
        # item["zufang_phone"] = response.xpath("//p[@class='content__aside__list--bottom oneline']/text()").extract_first()
        zufang_info = response.xpath("//div[@class='content__article__info']//ul/li/text()").extract()
        item["zufang_info"] = []
        for info in zufang_info:
            info_list = info.strip()
            if info_list != '':
                item["zufang_info"].append(info_list)
        item["zufang_ucid"] = response.xpath("//span[@class='agent__im']/@data-info").extract_first()
        price_url = 'https://bj.zu.ke.com/aj/house/brokers?house_codes={}&ucid={}'.format(item["zufang_house_codes"],item["zufang_ucid"])
        yield scrapy.Request(
            price_url,
            callback=self.parse_zufang_price,
            meta={"item": item}
        )

    def parse_zufang_price(self, response):
        item = response.meta["item"]
        item["zufang_master"] = json.loads(response.body.decode())['data'][item["zufang_house_codes"]][item["zufang_house_codes"]]["contact_name"]
        zufang_phone = json.loads(response.body.decode())['data'][item["zufang_house_codes"]][item["zufang_house_codes"]]["tp_number"]
        item["zufang_phone"] = re.sub(',','转',zufang_phone)
        yield item






