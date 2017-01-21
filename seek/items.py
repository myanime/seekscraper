# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SeekItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    advertiser_id = scrapy.Field()
    advertiser_description = scrapy.Field()
    suburbWhereValue = scrapy.Field()
    classification_description = scrapy.Field()
    subClassification_description = scrapy.Field()
    logo_ID = scrapy.Field()
    logo_description = scrapy.Field()
    listingDate = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    locationWhereValue = scrapy.Field()
    teaser = scrapy.Field()
    workType = scrapy.Field()
    salary = scrapy.Field()
    areaWhereValue = scrapy.Field()
    area = scrapy.Field()
    original_link_telephones = scrapy.Field()
    original_link_emails = scrapy.Field()
    salaryrange=scrapy.Field()
    postCode = scrapy.Field()


class JobID(scrapy.Item):
    url = scrapy.Field()