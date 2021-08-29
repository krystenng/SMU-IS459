
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['forums.hardwarezone.com.sg/forums/pc-gaming.382']
    start_urls = ['http://forums.hardwarezone.com.sg/forums/pc-gaming.382//']
    base_url = 'https://forums.hardwarezone.com.sg'

    def parse(self, response):

        all_the_threads = response.xpath('//div[starts-with(@class, "structItem structItem--thread js-inlineModContainer js-threadListItem-")]')

        # print(len(all_the_threads))
        for thread in all_the_threads:
            thread_url = self.base_url + thread.xpath('.//div[@class="structItem-title"]/a/@href').extract_first()
            # print(thread_url)
            yield scrapy.Request(thread_url, callback=self.parse_thread,dont_filter=True)

        next_page_partial_url = response.xpath('//li[@class="pageNav-page pageNav-page--later"]/a/@href').extract_first()
        next_page_url = self.base_url + next_page_partial_url
        yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)


    def parse_thread(self, response):

        # threads = response.xpath('//article[@class="message message--post js-post js-inlineModContainer  "]')
        # print(len(thread))

        next_page_partial_url = response.xpath('//li[@class="pageNav-page pageNav-page--later"]/a/@href').extract_first()
        if next_page_partial_url != None:
            threads = response.xpath('//article[@class="message message--post js-post js-inlineModContainer  "]')
            for thread in threads:
                name = response.xpath('//div/h1/text()').extract_first()
                content_list = thread.xpath('.//div[@class="bbWrapper"]/text()').extract()
                content = ''.join(content_list)
                # print(content)
                author = thread.xpath('.//h4/a/text()').extract_first()
                if author == None:
                    author = thread.xpath('.//h4/a/span/text()').extract_first()
                # print(author)
                yield {
                    'Name': name,
                    'Author': author,
                    'content': content
                }
            next_page_url = self.base_url + next_page_partial_url
            yield scrapy.Request(next_page_url, callback=self.parse_thread, dont_filter=True)

        else:
            threads = response.xpath('//article[@class="message message--post js-post js-inlineModContainer  "]')
            for thread in threads:
                name = response.xpath('//div/h1/text()').extract_first()
                content_list = thread.xpath('.//div[@class="bbWrapper"]/text()').extract()
                content = ''.join(content_list)
                # print(content)
                author = thread.xpath('.//h4/a/text()').extract_first()
                if author == None:
                    author = thread.xpath('.//h4/a/span/text()').extract_first()
                # print(author)
                yield {
                    'Name': name,
                    'Author': author,
                    'content': content
                }
        
            


