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
# from pyvirtualdisplay import Display
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

'''
class URLScraper(scrapy.Spider):
    name = "pc"
    all_urls=[]
    zips = [line.strip('\n') for line in open('./seek/spiders/zips')]
    for zip in zips:
        urls = 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&dateRange=1&where={0}'.format(zip)
        all_urls.append(urls)
    start_urls = all_urls

    def parse(self, response):
        import json
        jsonresponse = json.loads(response.body_as_unicode())
        postcode = response.url
        postcode = postcode.replace('https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&dateRange=1&where=','')
        parentLocation = jsonresponse['location']['suburbParentDescription']
        if parentLocation:
            with open('postcodes_map', 'a') as f:
                f.write(postcode)
                f.write(',')
                f.write(parentLocation)
                f.write('\n')
'''
class JobListScraper(scrapy.Spider):
    """
    scrapy crawl joblist -s DNS_TIMEOUT=3 -s DOWNLOAD_TIMEOUT=5 -o test21.csv
    """
    DAYS = 1
    name = "joblist"
    seek_pages = []
    salary_ranges = [0, 30000, 40000, 50000, 60000, 70000, 80000, 100000, 120000, 150000, 200000, 999999]
    for i in range(0, len(salary_ranges) - 1):
        for page in range(1, 100):
            seek_pages.append('https://www.seek.com.au/jobs/in-All-Australia?'
                              'daterange={3}&salaryrange={1}-{2}&salarytype=annual&page={0}'
                              .format(page, salary_ranges[i], salary_ranges[i+1],DAYS))

    start_urls = seek_pages

    def parse(self, response):
        print "#####################"
        print self.DAYS
        links = response.css("a[href*='/job/']").extract()
        urlprice = response.url
        urlprice = urlprice.replace('https://www.seek.com.au/jobs/in-All-Australia?daterange={0}&salaryrange='.format(self.DAYS), '')
        urlprice = urlprice.split('&')[0]
        for link in links:
            soup = BeautifulSoup(link)
            job = soup.find('a', href=True)['href']
            job = job.replace('/job/', '')
            job = job.split('?')[0]
            print job
            item = JobID()
            item['url'] = str(job) + ',' + urlprice
            yield item


class SeekScraper(scrapy.Spider):
    start_urls = ['https://www.google.com']
    name = "seek"
    # display = Display(visible=0, size=(800, 600))
    # display.start()

    def parse(self, response):
        with open('./static/output/joblist', 'r') as file:
            seek_ids = [line.rstrip('\n') for line in file]
            seek_ids = seek_ids[1:]

        def loadchromeProxy():
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

        def loadchrome():
            driver = webdriver.Chrome("./chromedriver")
            # driver = webdriver.Firefox()

            driver.get("http://www.google.com")
            return driver

        driver = loadchrome()
        time.sleep(10)

        for id in seek_ids:
            urlid = id.split(',')[0]
            salaryrange= id.split(',')[1]
            item = SeekItem()
            item['salaryrange'] = salaryrange
            url = "https://www.seek.com.au/job/" + urlid
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
                        print "###########################################################################"
                        print "###########################################################################"
                        print "###########################################################################"
                        print "###########################################################################"
                        print "###########################################################################"
                        print "############################### GOT BLOCKED ###############################"
                        print "###########################################################################"
                        print "###########################################################################"
                        print "###########################################################################"
                        print "###########################################################################"

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
                postCodeInt = []
                pcText = data['suburbWhereValue']
                postcodere = r'(0[289][0-9]{2})|([1345689][0-9]{3})|(2[0-8][0-9]{2})|(290[0-9])|(291[0-4])|(7[0-4][0-9]{2})|(7[8-9][0-9]{2})$'
                pcText = re.search(postcodere, pcText)
                postCodeInt.append(pcText.group())
                item['postCode'] = postCodeInt[0]
            except:
                item['postCode'] = ''
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
                item['teaser'] = data['teaser'].rstrip('\n')
            except:
                pass
            try:
                pass
                item['workType'] = data['workType']
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
