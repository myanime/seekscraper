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
        time.sleep(1)
        DAYS = 1
        salary_ranges = [0, 30000, 40000, 50000, 60000, 70000, 80000, 100000, 120000, 150000, 200000, 999999]
        salary_ranges = [30000, 100000]
        for i in range(0, 1):
        # for i in range(0, len(salary_ranges) - 1):
            salary_range_string = str(salary_ranges[i]) + "-" + str(salary_ranges[i + 1])
            for page in range(1, 2):
            # for page in range(1, 100):
                current_page = 'https://www.seek.com.au/jobs/in-All-Australia?' \
                               'daterange={3}&salaryrange={1}-{2}&salarytype=annual&page={0}' \
                    .format(page, salary_ranges[i], salary_ranges[i + 1], DAYS)
                # current_page = 'https://www.seek.com.au/jobs/in-All-Australia?daterange=1&salaryrange=0-100000&salarytype=annual&page=1'
                try:
                    driver.get(current_page)
                    time.sleep(5)
                    print(current_page)
                except TimeoutException:
                    with open('error_timeout.txt', 'a') as file:
                        file.write(time.strftime('%d.%m %H:%M'))
                        file.write("###################TIMEOUT##############")
                        file.write('\n')
                    driver.quit()
                    driver = self.load_chrome()
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
                links = driver.find_elements_by_xpath("//span/h1/a")

                for link in links:
                    job = link.get_attribute('href')
                    job = job.split('/job/')[1]
                    job = job.split('?')[0]
                    self.all_job_ids.append((job, salary_range_string))
                    print(job, salary_range_string)

        seen = set()
        self.job_ids = [x for x in self.all_job_ids if x[0] not in seen and not seen.add(x[0])]
        print(self.job_ids)
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
                print "###########################################################################"
                print "############################### GOT BLOCKED ###############################"
                print "###########################################################################"
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

    def parse(self, response):
        driver = self.load_chrome()
        self.warm_up(driver)

        seek_ids = self.job_ids
        for job_id, salary_range in seek_ids:
            try:
                item = SeekItem()
                item['salaryrange'] = salary_range.rstrip("\r")
                driver.get('https://www.seek.com.au/job/{}'.format(job_id))
                blocked = self.check_if_blocked(driver, job_id)
                if blocked:
                    driver.quit()
                    driver = self.load_chrome()
                    self.warm_up(driver)
                    continue

                item['text'] = self.find_element(driver, '//*[@data-automation="jobDescription"]')
                item['advertiser_description'] = self.find_element(driver, '//*[@data-automation="advertiser-name"]')
                item['title'] = self.find_element(driver, '//*[@data-automation="job-detail-title"]/span/h1')
                item['workType'] = self.get_first_element(driver, '//section/dl/dd[3]/span/span')
                item['suburbWhereValue'] = self.get_first_element(driver, '//dl/dd[2]/span/span/span')
                item['area'] = self.get_first_element(driver, '//section/dl/dd[2]/span/span/span')
                item['location'] = self.get_first_element(driver, '//dl/dd[2]/span/span/strong')
                item['subClassification_description'] = self.get_first_element(driver, '//section/dl/div/dd/span/span/span')
                item['classification_description'] = self.get_first_element(driver, '//section/dl/div/dd/span/span/strong')
                # item['postCode']
                # item['advertiser_id']
                # item['areaWhereValue']
                # item['id']
                # item['listingDate']
                # item['locationWhereValue']
                # item['logo_ID']
                # item['logo_description']
                # item['salary']

                if item['text']:
                    item = self.phone_and_email_parser(item)
                    yield item
            except TimeoutException:
                with open('error_timeout.txt', 'a') as file:
                    file.write(time.strftime('Day:%d Month:%m Time: %H:%M -'))
                    file.write("###################TIMEOUT MAIN Scraper##############")
                    file.write('\n')
                driver.quit()
                driver = self.load_chrome()
                continue
            except:
                traceback.print_exc()
                driver.quit()
                driver = self.load_chrome()
                self.warm_up(driver)
