import scrapy
import time
from seek.items import SeekItem
from bs4 import BeautifulSoup
class URLScraper(scrapy.Spider):
    name = "seek_money"
    job_ids = [u'32520233', u'32540103', u'32597245', u'32597244', u'32597243', u'32597241', u'32597240']
    start_urls = []
    for job in job_ids:
        start_urls.append('https://api.seek.com.au/v2/jobs/search?jobId={}'.format(job))
    def parse(self, response):
        import json
        jsonresponse = json.loads(response.body_as_unicode())
        print response.url
        if jsonresponse['totalCount'] > 0:
            data = jsonresponse['data']
            for listing in data:
                item = SeekItem()
                item["name"] = listing
                jobid = response.url.replace('https://api.seek.com.au/v2/jobs/search?jobId=', '')
                print "$$$$$$$$$$$$$$$$"
                print jobid
                request = scrapy.Request("https://www.seek.com.au/job/"+jobid, callback=self.get_template_text)
                request.meta['item'] = item
                yield request
    def get_template_text(self, response):
        item = response.meta['item']
        text = response.css('div.templatetext').extract_first()
        soup = BeautifulSoup(text)
        item['text'] = soup.get_text()

        #response.xpath('//*[@id="jobTemplate"]/div/div/div[2]/div[2]/text()') #'#
        #
        return item


        # if jsonresponse['totalCount'] > 20:
        #     urlfull = response.url
        #     tc = str(jsonresponse['totalCount'])
        #     with open('postcodes', 'a') as f:
        #         f.write(str(urlfull))
        #         f.write(':')
        #         f.write(tc)
        #         f.write('\n')