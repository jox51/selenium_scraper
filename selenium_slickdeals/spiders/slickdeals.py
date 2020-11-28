import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class SlickdealsSpider(scrapy.Spider):
    name = 'slickdeals'
    page_number = 0

    #Don't need arguments below because we are using selenium
    # allowed_domains = ['slickdeals.com']
    # start_urls = ['http://slickdeals.com/']

    def start_requests(self):
        url='https://slickdeals.net/computer-deals/'
        yield SeleniumRequest(
            url=url,
            wait_time=3,
            screenshot=True,
            callback=self.parse
        )

    def parse(self, response):

        driver = response.meta['driver']
        html = driver.page_source #grabs the page source
        response_obj = Selector(text=html) #turns page source into obj that can be selected via xpath/css etc

        computers = response_obj.xpath('//li[@class="fpGridBox grid altDeal hasPrice"]/div/div')
        for computer in computers:
            yield{
                'link': response.urljoin(computer.xpath('.//div[1]/@data-href').get()),
                'price': computer.xpath('normalize-space(.//div/div[@class="itemInfoLine"]/div/div/text())').get(),
                'store': computer.xpath('.//div/div/div/span[@class="blueprint"]/*/text()').get()
            }

        next_page = response_obj.xpath(' //div[@class="pagination buttongroup"]/*[@data-role="next-page"]')
        self.page_number += 1
        if next_page:
            next_page_url = f'https://slickdeals.net/computer-deals/?page={self.page_number}'
            yield SeleniumRequest(
                url=next_page_url,
                wait_time=1,
                callback=self.parse
            )





