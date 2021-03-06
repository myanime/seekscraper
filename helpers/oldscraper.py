import scrapy
import time
from seek.items import SeekItem, JobID
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import time
from pandas.io.json import json_normalize
import random
from selenium.webdriver.chrome.options import Options
import zipfile
import re
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""
background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "schlupfi.de",
            port: parseInt(3128)
          },
          bypassList: ["foobar.com"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "user1",
            password: "indeed"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
"""
'''
{
  "title": "Start a Job Search & Find a Dream Career - Jobs Posted Daily",
  "totalCount": 1,
  "data": [
    {
      "id": 32597245,
      "listingDate": "2017-01-15T19:53:51Z",
      "title": "Electrician",
      "teaser": "Looking for Electricians in the Central Coast",
      "bulletPoints": [

      ],
      "advertiser": {
        "id": "35085835",
        "description": "V Com"
      },
      "logo": {
        "id": "",
        "description": null
      },
      "isPremium": false,
      "isStandOut": false,
      "location": "Gosford & Central Coast",
      "area": "",
      "workType": "Full Time",
      "classification": {
        "id": "1225",
        "description": "Trades & Services"
      },
      "subClassification": {
        "id": "6230",
        "description": "Electricians"
      },
      "salary": "",
      "companyProfileStructuredDataId": 21991,
      "locationWhereValue": "Gosford & Central Coast NSW",
      "automaticInclusion": false,
      "displayType": "standard",
      "tracking": "ewogICJ0b2tlbiI6ICI2NTYzMmRjYi03ZDBjLTQ0MjAtYjI2ZC05NGU4OTg3ZTg1NmZfMSIKfQ=="
    }
  ],
  "paginationParameters": {
    "hadPremiumListings": false,
    "seekSelectAllPages": true
  },
  "info": {
    "timeTaken": 10,
    "source": "JobSearch-ES"
  },
  "userQueryId": "API4579572098423361657",
  "sortMode": [
    {
      "name": "Date",
      "value": "ListedDate",
      "isActive": true
    }
  ]
}
'''

class JobListScraper(scrapy.Spider):
    name = "joblist"
    seek_pages = []
    for page in range(1, 2):
        seek_pages.append('https://www.seek.com.au/jobs/in-All-Australia?daterange=3&page={}'.format(page))

    start_urls = seek_pages

    def parse(self, response):
        links = response.css("a[href*='/job/']").extract()
        for link in links:
            soup = BeautifulSoup(link)
            job = soup.find('a', href=True)['href']
            job = job.replace('/job/', '')
            job = job.split('?')[0]
            print job
            item = JobID()
            item['url'] = job
            yield item


class SeekScraper(scrapy.Spider):
    start_urls = ['https://www.google.com']
    name = "seek"

    def parse(self, response):
        with open('./static/output/joblist', 'r') as file:
            seek_ids = [line.rstrip('\n') for line in file]
            seek_ids = seek_ids[1:]

        def loadchrome():
            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)

            co = Options()
            co.add_argument("--start-maximized")
            co.add_extension(pluginfile)

            driver = webdriver.Chrome("./chromedriver", chrome_options=co)
            driver.get("http://www.google.com")
            return driver

        driver = loadchrome()
        time.sleep(10)

        for id in seek_ids:
            url = "https://www.seek.com.au/job/" + id
            try:
                # wait = random.randrange(10,15)
                # time.sleep(wait)
                driver.get(url)
                element = driver.find_element_by_css_selector('div.templatetext')
                text = element.text

                ############################################
                # EMAIL TELEPHONE PARSER
                emails = []
                telephone_numbers = []

                re_email = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
                re1 = r'(0[1-8]{1,1} [0-9]{3,5} [0-9]{3,5})'
                re2 = r'(\([0-9]{2,2}\).[0-9]{3,5}.[0-9]{3,5})'
                re3 = r'\+61.[0-9]{1,1}.[0-9]{2,5}.[0-9]{2,5}.[0-9]{2,5}'

                e1 = re.search(re_email, text, re.I)
                if e1:
                    emails.append(e1.group())
                t1 = re.search(re1, text, re.I)
                t2 = re.search(re2, text, re.I)
                t3 = re.search(re3, text, re.I)
                if t1:
                    telephone_numbers.append(t1.group())
                if t2:
                    telephone_numbers.append(t2.group())
                if t3:
                    telephone_numbers.append(t3.group())
                try:
                    item['original_link_emails'] = emails[0]
                except:
                    item['original_link_emails'] = 'None'
                try:
                    item['original_link_telephones'] = telephone_numbers[0]
                except:
                    item['original_link_telephones'] = ''

                    ######################################


            except:
                text = ''
                try:
                    if "blocked access" in driver.page_source:
                        with open('error.txt', 'a') as file:
                            file.write("Error\n")
                            file.write(url)
                            file.write('\n')
                        time.sleep(30)
                        driver.quit()
                        time.sleep(5)
                        driver = loadchrome()

                except:
                    pass

            item = SeekItem()
            item['text'] = text
            item['url'] = url

            apiurl = 'https://api.seek.com.au/v2/jobs/search?jobId={}'.format(id)
            request = scrapy.Request(apiurl, callback=self.get_json)
            request.meta['item'] = item
            yield request

    def get_json(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        if jsonresponse['totalCount'] > 0:
            data = jsonresponse['data'][0]
            # import time
            # time.sleep(10)
            item = response.meta['item']
            # df = json_normalize(data)
            # item['name'] = data #df.to_json()
            try:
                print data['advertiser']['id']
            except:
                pass
            print "############################"
            try:
                item['advertiser_id'] = data['advertiser']['id']
            except:
                pass
            try:
                item['advertiser_description'] = data['advertiser']['description']
            except:
                pass
            try:
                item['suburbWhereValue'] = data['suburbWhereValue']
            except:
                pass
            try:
                item['classification_description'] = data['classification']['description']
            except:
                pass
            try:
                item['subClassification_description'] = data['subClassification']['description']
            except:
                pass
            try:
                item['logo_ID'] = data['logo']['id']
            except:
                pass
            try:
                item['logo_description'] = data['logo']['description']
            except:
                pass
            try:
                item['listingDate'] = data['listingDate']
            except:
                pass
            try:
                item['id'] = data['id']
            except:
                pass
            try:
                item['title'] = data['title']
            except:
                pass
            try:
                item['location'] = data['location']
            except:
                pass
            try:
                item['locationWhereValue'] = data['locationWhereValue']
            except:
                pass
            try:
                item['teaser'] = data['teaser']
            except:
                pass
            try:
                pass
                # item['workType'] = data['workType']
            except:
                pass
            try:
                item['salary'] = data['salary']
            except:
                pass
            try:
                item['areaWhereValue'] = data['areaWhereValue']
            except:
                pass
            try:
                item['area'] = data['area']
            except:
                pass

            return item

