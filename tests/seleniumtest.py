import re
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def load_chrome():
    driver = webdriver.Chrome("./chromedriver")
    driver.set_page_load_timeout(10)
    return driver


def check_if_blocked(driver, job_id):
    try:
        if "blocked access" in driver.page_source:
            print "###########################################################################"
            print "############################### GOT BLOCKED ###############################"
            print "###########################################################################"

            with open('error.txt', 'a') as file:
                file.write(time.strftime('Day:%d Month:%m Time: %H:%M -'))
                file.write(job_id)
                file.write('\n')
            return True
    except:
        traceback.print_exc()


def phone_and_email_parser(item):
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


def warm_up(driver):
    driver.get('https://www.seek.com.au/job/38226458')
    time.sleep(5)


example_job_list = [
    "38226458",
    "38341779",
    "38273443",
    "38316054",
    "38295104",
    "38302885",
    "38292661",
    "38159962",
    "38151424",
    "38108196",
    "38329187",
    "38157831",
    "38271395",
    "38263267",
    "38302739",
    "38232633",
    "38320303",
    "38290840"
]

example_job_list = [(u'38929769', '30000-100000'), (u'38946309', '30000-100000'), (u'38945947', '30000-100000')]#, (u'38390553', '30000-100000'), (u'38390549', '30000-100000'), (u'38390502', '30000-100000'), (u'38390501', '30000-100000'), (u'38390503', '30000-100000'), (u'38390548', '30000-100000'), (u'38390512', '30000-100000'), (u'38390573', '30000-100000'), (u'38390493', '30000-100000'), (u'38390544', '30000-100000'), (u'38390492', '30000-100000'), (u'38390561', '30000-100000'), (u'38390517', '30000-100000'), (u'38390516', '30000-100000'), (u'38390532', '30000-100000'), (u'38390530', '30000-100000'), (u'38390484', '30000-100000'), (u'38390540', '30000-100000'), (u'38390542', '30000-100000')]

driver = load_chrome()

jobs = []
for job_id, salary_range in example_job_list:
    try:
        def find_element(xpath):
            try:
                element = driver.find_element_by_xpath(xpath)
                text = element.text
                return text
            except NoSuchElementException:
                pass
            except:
                pass

        def get_first_element(xpath):
            try:
                element = driver.find_elements_by_xpath(xpath)[1]
                text = element.text
                return text
            except NoSuchElementException:
                pass
            except:
                pass

        driver.get('https://www.seek.com.au/job/{}'.format(job_id))

        blocked = check_if_blocked(driver, job_id)
        if blocked:
            driver.quit()
            driver = load_chrome()
            warm_up(driver)
            continue

        item = {}
        item['teaser'] = driver.find_element_by_xpath('/html/head/meta[4]').get_attribute('content')
        # fake_api = driver.find_element_by_xpath('//*[@data-automation="server-state"]').get_attribute('innerHTML')
        # decoded_fake_api = fake_api.encode('utf8').decode('unicode-escape').lstrip('\n window.SEEK_CONFIG=')
        fake_api = driver.find_element_by_xpath('//*[@data-automation="server-state"]').get_attribute('innerHTML').split('SEEK_REDUX_DATA = ')[1].split('window.SK_DL')[0].rstrip(' ').rstrip('\n').rstrip(';')
        import json
        fake_api_dict = json.loads(fake_api)
        city = json.loads(fake_api)['jobdetails']['result']['locationHierarchy']['city']
        area = json.loads(fake_api)['jobdetails']['result']['locationHierarchy']['area']
        suburb = json.loads(fake_api)['jobdetails']['result']['locationHierarchy']['suburb']
        print(city,area,suburb,item['teaser'])
        item['text'] = find_element('//*[@data-automation="jobDescription"]')
        item['advertiser_description'] = find_element('//*[@data-automation="advertiser-name"]')
        if not item['advertiser_description']:
            item['advertiser_description'] = find_element('//*[@data-automation="job-header-company-review-title"]')
        if not item['advertiser_description']:
            item['advertiser_description'] = 'Private Advertiser'
        item['title'] = find_element('//*[@data-automation="job-detail-title"]/span/h1')

        item['workType'] = get_first_element('//section/dl/dd[3]/span/span')
        item['suburbWhereValue'] = get_first_element('//dl/dd[2]/span/span/span')
        item['area'] = get_first_element('//section/dl/dd[2]/span/span/span')
        item['location'] = get_first_element('//dl/dd[2]/span/span/strong')
        item['subClassification_description'] = get_first_element('//section/dl/div/dd/span/span/span')
        item['classification_description'] = get_first_element('//section/dl/div/dd/span/span/strong')

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
            item = phone_and_email_parser(item)
            jobs.append(item)
    except TimeoutException:
        with open('error_timeout.txt', 'a') as file:
            file.write(time.strftime('Day:%d Month:%m Time: %H:%M -'))
            file.write("###################TIMEOUT MAIN Scraper##############")
            file.write('\n')
        driver.quit()
        driver = load_chrome()
        continue
    except:
        traceback.print_exc()
        driver.quit()
        driver = load_chrome()
        warm_up(driver)

print(jobs)
