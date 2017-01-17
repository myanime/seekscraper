from selenium import webdriver
import json
import time
from pandas.io.json import json_normalize

def main():
    start_urls = ["https://www.seek.com.au/job/" + line.rstrip('\n') for line in open('./seek/spiders/joblist', 'r')]
    print start_urls
    driver = webdriver.Chrome(executable_path='./chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=' + 'schlupfi.de:3128')
    driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
    driver.get('https://www.seek.com.au')
    time.sleep(10)
    for url in start_urls:
    # def worker(url):
        try:
            driver.get(url)
            element = driver.find_element_by_css_selector('div.templatetext')
            text = element.text
            print text
        except:
            pass

def main3():
    # driver.findElement(By.cssSelector("a[href*='long']")).click();
    driver = webdriver.Chrome(executable_path="./chromedriver")
    jobids=[]
    for page in range(1, 500):
        driver.get('https://www.seek.com.au/jobs/in-All-Australia?daterange=3&page={}'.format(page))
        linke = driver.find_elements_by_css_selector("a[href*='/job/']")
        for i in linke:
            job = i.get_attribute("href")
            job = job.replace('https://www.seek.com.au/job/', '')
            job = job.split('?')[0]
            jobids.append(job)
            print job
    print jobids
def main2():
    driver = webdriver.Chrome(executable_path="./chromedriver")
    x = 1
    all_jobs = []

    zips = [line.strip('\n') for line in open('./seek/spiders/zips')]
    postcodes = [line.strip('\n') for line in open('./seek/spiders/postcodes')]
    all_urls = []
    for zip in zips:
        urls = 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where={0}&dateRange=1'.format(zip)
        all_urls.append(urls)
    for zip in postcodes:
        all_urls.append('https://api.seek.com.au/v2/jobs/search?salaryRange=0-10000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=10000-20000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=20000-30000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=30000-40000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=40000-50000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=50000-60000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=60000-70000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=70000-80000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=80000-90000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=90000-100000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=100000-120000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=120000-150000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=150000-200000&where={0}&dateRange=1'.format(zip))
        all_urls.append(
            'https://api.seek.com.au/v2/jobs/search?salaryRange=200000-999999&where={0}&dateRange=1'.format(zip))
    with open('wawaaw', 'w') as d:
        json.dump(all_urls,d)
    for url in all_urls:
        # print url
        driver.get(url)
        data = driver.find_element_by_xpath('/html/body/pre').text

        new_jobs = json.loads(data)
        jobsect= new_jobs['totalCount']
        if jobsect:
            print jobsect
            new_jobs = new_jobs['data']
            print len(all_jobs), x
            all_jobs = all_jobs + new_jobs
            # print all_jobs
            all_jobs = {each['id']: each for each in all_jobs}.values()

        x = x + 1
        # time.sleep(2)
    unique = {each['id']: each for each in all_jobs}.values()

    with open('tmp', 'w') as data:
        json.dump(unique, data)

    df = json_normalize(unique)
    df = df.drop_duplicates('id')
    df = df.sort('id')
    today = time.strftime('_%d_%m_%Y')
    filename = './seek_seleniumsplit{0}.csv'.format(today)
    df.to_csv(filename, encoding='utf-8')

    print len(unique)

    """

    for zip in all_urls:
        driver.get(url)
        data = driver.find_element_by_xpath('/html/body/pre').text

        new_jobs = json.loads(data)
        print new_jobs['totalCount']
        if new_jobs:
            new_jobs = new_jobs['data']
            print len(all_jobs), x
            all_jobs = all_jobs + new_jobs
            # print all_jobs
            all_jobs = {each['id']: each for each in all_jobs}.values()

        x = x + 1
        # time.sleep(1)
    unique = {each['id']: each for each in all_jobs}.values()

    with open('tmp', 'w') as data:
        json.dump(unique, data)

    df = json_normalize(unique)
    df = df.drop_duplicates('id')
    df = df.sort('id')
    today = time.strftime('_%d_%m_%Y')
    filename = './seek_seleniumsplit{0}.csv'.format(today)
    df.to_csv(filename, encoding='utf-8')

    print len(unique)
    """
    '''
    while x < 200:
        wageLower = x*500
        wageUpper = wageLower + 500
        print wageLower,wageUpper
        driver.get('https://api.seek.com.au/v2/jobs/search?salaryRange={0}-{1}&dateRange=3'.format(wageLower, wageUpper))
        data = driver.find_element_by_xpath('/html/body/pre').text

        new_jobs= json.loads(data)
        print new_jobs['totalCount']
        if new_jobs:
            new_jobs=new_jobs['data']
            print len(all_jobs), x
            all_jobs = all_jobs + new_jobs
            # print all_jobs
            all_jobs = {each['id']: each for each in all_jobs}.values()

        x = x + 1
        # time.sleep(1)
    unique = {each['id']: each for each in all_jobs}.values()

    with open('tmp', 'w') as data:
        json.dump(unique,data)

    df = json_normalize(unique)
    df = df.drop_duplicates('id')
    df = df.sort('id')
    today = time.strftime('_%d_%m_%Y')
    filename = './seek_seleniumsplit{0}.csv'.format(today)
    df.to_csv(filename, encoding='utf-8')

    print len(unique)
    '''
if __name__ == "__main__":
    main()
