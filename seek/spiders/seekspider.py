import re
import time
import traceback

import scrapy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from seek.items import SeekItem

example_job_list = [
    ("38226458", "payrange222"),
    ("38341779", "payrange222"),
    ("38273443", "payrange222"),
    ("38316054", "payrange222"),
    ("38295104", "payrange222"),
    ("38302885", "payrange222"),
    ("38292661", "payrange222"),
    ("38159962", "payrange222"),
    ("38151424", "payrange222"),
]

DEBUG = False

class SeekScraper(scrapy.Spider):
    start_urls = ['https://www.google.com']
    name = "seek"

    def __init__(self, *args, **kwargs):
        self.all_job_ids = []
        self.job_ids = example_job_list if DEBUG else None
        if not DEBUG:
            self.get_jobs_and_set_job_ids()
        super(SeekScraper, self).__init__(*args, **kwargs)

    def get_jobs_and_set_job_ids(self):
        driver = self.load_chrome()
        self.warm_up(driver)
        DAYS = 1
        salary_ranges = [0, 30000, 40000, 50000, 60000, 70000, 80000, 100000, 120000, 150000, 200000, 999999]
        # salary_ranges = [30000, 100000]
        # for i in range(0, 1):
        for i in range(0, len(salary_ranges) - 1):
            salary_range_string = str(salary_ranges[i]) + "-" + str(salary_ranges[i + 1])
            # for page in range(1, 2):
            for page in range(1, 100):
                current_page = 'https://www.seek.com.au/jobs/in-All-Australia?' \
                               'daterange={3}&salaryrange={1}-{2}&salarytype=annual&page={0}' \
                    .format(page, salary_ranges[i], salary_ranges[i + 1], DAYS)
                # current_page = 'https://www.seek.com.au/jobs/in-All-Australia?daterange=1&salaryrange=0-100000&salarytype=annual&page=1'
                try:
                    driver.get(current_page)
                    time.sleep(2)
                    driver.execute_script("window.stop();")
                    print(current_page)
                except TimeoutException:
                    with open('error_timeout.txt', 'a') as file:
                        file.write(time.strftime('%d.%m %H:%M'))
                        file.write("###################TIMEOUT##############")
                        file.write('\n')
                    # driver.quit()
                    # driver = self.load_chrome()
                    # driver.execute_script("window.stop();")
                    continue

                if "we couldn't find anything" in driver.page_source:
                    print("Moving on to next salary level")
                    break
                blocked = self.check_if_blocked(driver, 'getting ids')
                if blocked:
                    driver.quit()
                    driver = self.load_chrome()
                    self.warm_up(driver)
                    continue

                try:
                    links = driver.find_elements_by_xpath("//span/h1/a")

                    for link in links:
                        job = link.get_attribute('href')
                        job = job.split('/job/')[1]
                        job = job.split('?')[0]
                        self.all_job_ids.append((job, salary_range_string))
                        print(job, salary_range_string)
                except:
                    continue

        seen = set()
        self.job_ids = [x for x in self.all_job_ids if x[0] not in seen and not seen.add(x[0])]
        # print(self.job_ids)
        with open('job_ids.txt', 'a') as file:
            file.write(str(self.job_ids))
        time.sleep(30)

    def load_chrome(self):
        driver = webdriver.Chrome("./chromedriver")
        driver.set_page_load_timeout(10)
        return driver

    def check_if_blocked(self, driver, job_id):
        try:
            if "blocked access" in driver.page_source:
                print("###########################################################################")
                print("############################### GOT BLOCKED ###############################")
                print("###########################################################################")
                with open('error_blocked.txt', 'a') as file:
                    file.write(time.strftime('Day:%d Month:%m Time: %H:%M -'))
                    file.write(job_id)
                    file.write('\n')
                return True
        except:
            traceback.print_exc()

    def phone_and_email_parser(self, item):
        text = item['text']
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
        return item

    def warm_up(self, driver):
        driver.get('https://www.seek.com.au/job/38226458')
        time.sleep(5)

    def get_first_element(self, driver, xpath):
        try:
            element = driver.find_elements_by_xpath(xpath)[1]
            text = element.text
            return text
        except NoSuchElementException:
            pass
        except:
            pass

    def find_element(self, driver, xpath):
        try:
            element = driver.find_element_by_xpath(xpath)
            text = element.text
            return text
        except NoSuchElementException:
            pass
        except:
            pass

    def post_code_generator(self, location):
        standardPostcode = [('Alice Springs & Central Australia', 872),
                            ('Brisbane', 4000),
                            ('Darwin', 800),
                            ('Melbourne', 3000),
                            ('Perth', 6000),
                            ('Sydney', 2000),
                            ('Katherine & Northern Australia', 850),
                            ('Adelaide Hills & Barossa', 5131),
                            ('Albany & Great Southern', 6316),
                            ('Albury Wodonga & Murray', 2640),
                            ('Albury Area', 2640),
                            ('Adelaide', 5000),
                            ('Canberra', 2600),
                            ('Gold Coast', 4207),
                            ('Hobart', 7000),
                            ('Bairnsdale & Gippsland', 3847),
                            ('Ballarat & Central Highlands', 3321),
                            ('Bayside & Eastern Suburbs Brisbane', 4157),
                            ('Bayside & South Eastern Suburbs Melbourne', 3145),
                            ('Bendigo, Goldfields & Macedon Ranges', 3334),
                            ('Blue Mountains & Central West', 2773),
                            ('Brisbane CBD & Inner Suburbs Brisbane', 4000),
                            ('Broome & Kimberley', 6725),
                            ('Bunbury & South West', 6218),
                            ('Bundaberg & Wide Bay Burnett', 4621),
                            ('Cairns & Far North', 4849),
                            ('Central & South East TAS', 7027),
                            ('Coffs Harbour & North Coast', 2441),
                            ('Coober Pedy & Outback SA', 5440),
                            ('Devonport & North West', 7256),
                            ('Dubbo & Central NSW', 2357),
                            ('Eastern Suburbs Melbourne', 3101),
                            ('Eastern Suburbs Perth', 6051),
                            ('Far West & North Central NSW', 2386),
                            ('Fleurieu Peninsula & Kangaroo Island', 5157),
                            ('Fremantle & Southern Suburbs Perth', 6102),
                            ('Geelong & Great Ocean Road', 3212),
                            ('Geraldton, Gascoyne & Midwest', 6513),
                            ('Gladstone & Central QLD', 4420),
                            ('Gosford & Central Coast', 2083),
                            ('Goulburn & Southern Tablelands', 2575),
                            ('Southern Highlands & Tablelands', 2575),
                            ('Hervey Bay & Fraser Coast', 4570),
                            ('Horsham & Grampians', 3293),
                            ('Kalgoorlie, Goldfields & Esperance', 6429),
                            ('Launceston & North East', 7190),
                            ('Lismore & Far North Coast', 2469),
                            ('Mackay & Coalfields', 4705),
                            ('Mandurah & Peel', 6121),
                            ('Melbourne CBD & Inner Suburbs Melbourne', 3000),
                            ('Mildura & Murray', 3490),
                            ('Mornington Peninsula & Bass Coast', 3911),
                            ('Mt Gambier & Limestone Coast', 5259),
                            ('Mt Isa & Western', 4417),
                            ('Newcastle, Maitland & Hunter', 2264),
                            ('North Shore & Northern Beaches Sydney', 2060),
                            ('North West & Hills District Sydney', 2077),
                            ('Northam & Wheatbelt', 6041),
                            ('Northern Suburbs & Joondalup Perth', 6017),
                            ('Northern Suburbs Brisbane', 4019),
                            ('Northern Suburbs Melbourne', 3043),
                            ('Parramatta & Western Suburbs Sydney', 2116),
                            ('Perth CBD, Inner & Western Suburbs Perth', 6000),
                            ('Port Hedland, Karratha & Pilbara', 6710),
                            ('Port Macquarie & Mid North Coast', 2424),
                            ('Richmond & Hawkesbury', 2753),
                            ('Riverland & Murray Mallee', 5236),
                            ('Rockhampton & Capricorn Coast', 4699),
                            ('Rockingham & Kwinana Perth', 6165),
                            ('Ryde & Macquarie Park Sydney', 2112),
                            ('Shepparton & Goulburn Valley', 3558),
                            ('Somerset & Lockyer', 4311),
                            ('South West & M5 Corridor Sydney', 2162),
                            ('Southern Suburbs & Logan Brisbane', 4114),
                            ('Southern Suburbs & Sutherland Shire Sydney', 2133),
                            ('Sunshine Coast', 4517),
                            ('Sydney CBD, Inner West & Eastern Suburbs Sydney', 2000),
                            ('Tamworth & North West NSW', 2338),
                            ('Toowoomba & Darling Downs', 4350),
                            ('Townsville & Northern', 4800),
                            ('Traralgon & La Trobe Valley', 3781),
                            ('Tumut, Snowy & Monaro', 2621),
                            ('Wagga Wagga & Riverina', 2590),
                            ('Western Suburbs & Ipswich Brisbane', 4300),
                            ('Western Suburbs Melbourne', 3011),
                            ('Whyalla & Eyre Peninsula', 5600),
                            ('Wollongong, Illawarra & South Coast', 2500),
                            ('Yarra Valley & High Country', 3116),
                            ('Yorke Peninsula & Clare Valley', 5374),
                            ('South West Coast VIC', 3220),
                            ('West Gippsland & Latrobe Valley', 3844),
                            ('ACT', 2601),
                            ]
        found = False
        for city, postcode in standardPostcode:
            if location == city:
                return postcode
        if not found:
            with open('error_postcode.txt', 'a') as file:
                file.write(time.strftime('Day:%d Month:%m Time: %H:%M -'))
                file.write(city)
                file.write('\n')
        return ''

    def get_teaser(self, driver):
        try:
            return driver.find_element_by_xpath('/html/head/meta[4]').get_attribute('content')
        except:
            return ''

    def fake_api(self, driver):
        import json
        try:
            fake_api = driver.find_element_by_xpath('//*[@data-automation="server-state"]').get_attribute('innerHTML')
            fake_api_split = fake_api.split('SEEK_REDUX_DATA = ')[1].split('window.SK_DL')[0].rstrip(' ').rstrip('\n').rstrip(';')
            fake_api_dict = json.loads(fake_api_split)
            return fake_api_dict
        except:
            pass

    def extract_data(self, driver, job_id, item):
        item['text'] = self.find_element(driver, '//*[@data-automation="jobDescription"]')
        item['advertiser_description'] = self.find_element(driver, '//*[@data-automation="advertiser-name"]')
        if not item['advertiser_description']:
            item['advertiser_description'] = self.find_element(driver, '//*[@data-automation="job-header-company-review-title"]')
        if not item['advertiser_description']:
            item['advertiser_description'] = u'Private Advertiser'
        item['title'] = self.find_element(driver, '//*[@data-automation="job-detail-title"]/span/h1')
        item['workType'] = self.get_first_element(driver, '//section/dl/dd[3]/span/span')
        item['area'] = self.get_first_element(driver, '//section/dl/dd[2]/span/span/span')
        item['location'] = self.get_first_element(driver, '//dl/dd[2]/span/span/strong')
        item['subClassification_description'] = self.get_first_element(driver, '//section/dl/div/dd/span/span/span')
        item['classification_description'] = self.get_first_element(driver, '//section/dl/div/dd/span/span/strong')
        item['postCode'] = self.post_code_generator(item['location'])

        api_info = self.fake_api(driver)
        try:
            area = api_info['jobdetails']['result']['locationHierarchy']['area']
        except:
            area = ''
        try:
            suburb = api_info['jobdetails']['result']['locationHierarchy']['suburb']
        except:
            suburb = ''
        try:
            state = api_info['jobdetails']['result']['locationHierarchy']['state']
        except:
            state = ''
        try:
            salary = api_info['jobdetails']['result']['salary']
        except:
            salary = ''
        try:
            listing_date = api_info['jobdetails']['result']['listingDate']
        except:
            listing_date = ''
        try:
            advertiser_id = api_info['jobdetails']['result']['advertiser']['id']
        except:
            advertiser_id = ''

        item['locationWhereValue'] = state
        item['suburbWhereValue'] = suburb
        item['areaWhereValue'] = area

        item['advertiser_id'] = advertiser_id
        item['id'] = job_id
        item['listingDate'] = listing_date
        item['logo_ID'] = ''
        item['logo_description'] = ''
        item['salary'] = salary
        item['teaser'] = self.get_teaser(driver)
        item['url'] = 'https://www.seek.com.au/job/{}'.format(job_id)
        # item['standardPostcode']=item['postCode']

        if item['text']:
            item = self.phone_and_email_parser(item)
        return item

    def parse(self, response):
        driver = self.load_chrome()
        self.warm_up(driver)

        seek_ids = self.job_ids
        original_count = len(seek_ids)
        count = len(seek_ids)
        for job_id, salary_range in seek_ids:
            print("##########################")
            print("##########################")
            print("######## COUNT ###########")
            print("{}/{}".format(count, original_count))
            count=count-1
            print("##########################")
            print("##########################")
            print("##########################")
            print("##########################")
            print("##########################")
            try:
                item = SeekItem()
                item['salaryrange'] = salary_range.rstrip("\r")
                driver.set_page_load_timeout(10)
                driver.get('https://www.seek.com.au/job/{}'.format(job_id))
                blocked = self.check_if_blocked(driver, job_id)
                if blocked:
                    driver.quit()
                    driver = self.load_chrome()
                    self.warm_up(driver)
                    continue

                item = self.extract_data(driver, job_id, item)

                yield item

            except TimeoutException:
                with open('error_timeout.txt', 'a') as file:
                    file.write(time.strftime('Day:%d Month:%m Time: %H:%M -'))
                    file.write("###################TIMEOUT MAIN Scraper##############")
                    file.write('\n')
                # driver.quit()
                # driver = self.load_chrome()

                try:
                    time.sleep(5)
                    driver.execute_script("window.stop();")
                    item = self.extract_data(driver, job_id, item)
                    yield item
                except:
                    continue
                continue
            except Exception as e:
                traceback.print_exc()
                # driver.execute_script("window.stop();")
                # driver.quit()
                # driver = self.load_chrome()
                # self.warm_up(driver)
