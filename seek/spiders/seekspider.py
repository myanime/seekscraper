import scrapy
from seek.items import SeekItem
from selenium import webdriver
import json
import time
from selenium.webdriver.chrome.options import Options
import zipfile
import re
import traceback
import requests

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

class SeekScraper(scrapy.Spider):
    start_urls = ['https://www.google.com']
    name = "seek"

    def __init__(self, *args, **kwargs):
        self.all_job_ids = []
        driver = self.loadchrome()
        time.sleep(1)
        DAYS = 1
        salary_ranges = [0, 30000, 40000, 50000, 60000, 70000, 80000, 100000, 120000, 150000, 200000, 999999]
        # salary_ranges = [0, 30000]
        # for i in range(0, 1):
        for i in range(0, len(salary_ranges) - 1):
            salary_range_string = str(salary_ranges[i]) + "-" + str(salary_ranges[i + 1])
            # for page in range(1, 2):
            for page in range(1, 100):
                current_page = 'https://www.seek.com.au/jobs/in-All-Australia?' \
                               'daterange={3}&salaryrange={1}-{2}&salarytype=annual&page={0}' \
                    .format(page, salary_ranges[i], salary_ranges[i + 1], DAYS)
                driver.get(current_page)
                if "we couldn't find anything" in driver.page_source:
                    print("Moving on to next salary level")
                    break
                if "blocked access" in driver.page_source:
                    print "###########################################################################"
                    print "############################### GOT BLOCKED ###############################"
                    print "###########################################################################"
                    time.sleep(5)
                    driver.quit()
                    time.sleep(5)
                    driver = self.loadchrome()

                links = driver.find_elements_by_xpath("//span/h1/a")
                urlprice = str(salary_ranges[i] + salary_ranges[i + 1])
                for link in links:
                    job = link.get_attribute('href')
                    job = job.split('/job/')[1]
                    job = job.split('?')[0]
                    self.all_job_ids.append((job, salary_range_string))
                    print(job, salary_range_string)

        seen = set()
        self.job_ids = [x for x in self.all_job_ids if x[0] not in seen and not seen.add(x[0])]

        super(SeekScraper, self).__init__(*args, **kwargs)

    def loadchrome(self):
        driver = webdriver.Chrome("./chromedriver")
        driver.get("http://www.google.com")
        return driver

    def loadchromeProxy(self):
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

    def parse(self, response):
        driver = self.loadchrome()
        time.sleep(3)
        seek_ids = self.job_ids
        for id in seek_ids:
            urlid = id[0]
            salaryrange= id[1]
            item = SeekItem()
            item['salaryrange'] = salaryrange.rstrip("\r")
            url = "https://www.seek.com.au/job/" + urlid
            try:
                driver.get(url)
                element = driver.find_element_by_css_selector('div.templatetext')
                text = element.text
                print "############################"
                print "###########TEXT#############"
                print "############################"
                # print text
                # print "############################"

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
            except:
                traceback.print_exc()
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
                        driver = self.loadchrome()

                except:
                    traceback.print_exc()

            item['text'] = text
            item['url'] = url

            apiurl = 'https://api.seek.com.au/v2/jobs/search?jobId={}'.format(urlid)
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            print(apiurl)
            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
            r = requests.get(apiurl)
            created = False
            if r.status_code == 200:
                print("#######################################")
                print("###########SUCCESSFUL REQUEST##########")
                print("#######################################")
                jsonresponse = r.json()
                created, item = self.get_json(jsonresponse, item)
            if created:
                yield item
            else:
                with open('request_error.txt', 'a') as error_file:
                    error_file.write(time.strftime('%d.%m %H:%M'))
                    error_file.write(apiurl)
                    error_file.write('\n')


    def get_json(self, jsonresponse, item):
        def level_1(attrname, item, data):
            try:
                item[attrname] = data[attrname]
            except:
                traceback.print_exc()
        def level_2(attr1name, attr2name, attr3name, item, data):
            try:
                item[attr1name] = data[attr2name][attr3name]
            except:
                traceback.print_exc()
        if jsonresponse['totalCount'] == 1:
            data = jsonresponse['data'][0]

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
                item['teaser'] = data['teaser'].rstrip('\n').rstrip("\r").rstrip("\r").rstrip("\r")
            except:
                traceback.print_exc()

            level_2('advertiser_description', 'advertiser', 'description', item, data)
            level_2('advertiser_id', 'advertiser', 'id', item, data)
            level_1('area', item, data)
            level_1('areaWhereValue', item, data)
            level_2('classification_description', 'classification', 'description', item, data)
            level_1('id', item, data)
            level_1('listingDate', item, data)
            level_1('location', item, data)
            level_1('locationWhereValue', item, data)
            level_2('logo_ID', 'logo', 'id', item, data)
            level_2('logo_description', 'logo', 'description', item, data)
            level_1('salary', item, data)
            level_2('subClassification_description', 'subClassification', 'description', item, data)
            level_1('suburbWhereValue', item, data)
            level_1('title', item, data)
            level_1('workType', item, data)

            return True, item
        return False, item
