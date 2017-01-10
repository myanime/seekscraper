import scrapy
import time
from seek.items import SeekItem

class URLScraper(scrapy.Spider):
    name = "seek_ss"
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

    start_urls = all_urls
    # start_urls = ['https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=5000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6799&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2850&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3737&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4613&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2176&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2046&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4670&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3067&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7315&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=8006&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7112&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4627&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2795&dateRange=1']

    def parse(self, response):
        import json
        jsonresponse = json.loads(response.body_as_unicode())
        print response.url
        if jsonresponse['totalCount'] > 0:
            data = jsonresponse['data']
            for listing in data:
                item = SeekItem()
                item["name"] = listing
                yield item
        if jsonresponse['totalCount'] > 20:
            urlfull = response.url
            tc = str(jsonresponse['totalCount'])
            with open('postcodes', 'a') as f:
                f.write(str(urlfull))
                f.write(':')
                f.write(tc)
                f.write('\n')
class URLScraper1(scrapy.Spider):
    name = "seek_1"
    zips = [line.strip('\n') for line in open('./seek/spiders/zips')]
    postcodes = [line.strip('\n') for line in open('./seek/spiders/postcodes')]
    all_urls = []
    for zip in zips:
        urls = 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where={0}&dateRange=1'.format(zip)
        all_urls.append(urls)

    start_urls = all_urls

    # start_urls = ['https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=5000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6799&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2850&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3737&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4613&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2176&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2046&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4670&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3067&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7315&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=8006&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7112&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4627&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2795&dateRange=1']

    def parse(self, response):
        import json
        jsonresponse = json.loads(response.body_as_unicode())
        print response.url
        if jsonresponse['totalCount'] > 0:
            data = jsonresponse['data']
            for listing in data:
                item = SeekItem()
                item["name"] = listing
                yield item
        if jsonresponse['totalCount'] > 20:
            urlfull = response.url
            tc = str(jsonresponse['totalCount'])
            with open('postcodes', 'a') as f:
                f.write(str(urlfull))
                f.write(':')
                f.write(tc)
                f.write('\n')

class URLScraper2(scrapy.Spider):
    name = "seek_2"
    zips = [line.strip('\n') for line in open('./seek/spiders/zips2')]
    postcodes = [line.strip('\n') for line in open('./seek/spiders/postcodes')]
    all_urls = []
    for zip in zips:
        urls = 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where={0}&dateRange=1'.format(zip)
        all_urls.append(urls)

    start_urls = all_urls

    # start_urls = ['https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=5000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6799&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2850&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3737&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4613&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2176&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2046&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4670&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3067&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7315&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=8006&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7112&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4627&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2795&dateRange=1']

    def parse(self, response):
        import json
        jsonresponse = json.loads(response.body_as_unicode())
        print response.url
        if jsonresponse['totalCount'] > 0:
            data = jsonresponse['data']
            for listing in data:
                item = SeekItem()
                item["name"] = listing
                yield item
        if jsonresponse['totalCount'] > 20:
            urlfull = response.url
            tc = str(jsonresponse['totalCount'])
            with open('postcodes', 'a') as f:
                f.write(str(urlfull))
                f.write(':')
                f.write(tc)
                f.write('\n')

class URLScraper3(scrapy.Spider):
    name = "seek_3"
    postcodes = [line.strip('\n') for line in open('./seek/spiders/postcodes')]
    all_urls = []
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

    start_urls = all_urls
    # start_urls = ['https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=5000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6000&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6799&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2850&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=6280&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3737&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4613&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2176&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2046&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4670&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=3067&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7315&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=8006&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=7112&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=4627&dateRange=1', 'https://api.seek.com.au/v2/jobs/search?salaryRange=0-999999&where=2795&dateRange=1']

    def parse(self, response):
        import json
        jsonresponse = json.loads(response.body_as_unicode())
        print response.url
        if jsonresponse['totalCount'] > 0:
            data = jsonresponse['data']
            for listing in data:
                item = SeekItem()
                item["name"] = listing
                yield item
        if jsonresponse['totalCount'] > 20:
            urlfull = response.url
            tc = str(jsonresponse['totalCount'])
            with open('postcodes', 'a') as f:
                f.write(str(urlfull))
                f.write(':')
                f.write(tc)
                f.write('\n')


