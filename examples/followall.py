from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess


class FoolowAllSpider(Spider):
    """
    Follow all links
    """

    name = "follow"
    allowed_domains = ["quotes.toscrape.com"]

    def start_requests(self):
        yield Request(
            url="http://quotes.toscrape.com",
            meta={"playwright": True},
        )

    def parse(self, response):
        yield from response.follow_all(css="a", meta={"playwright": True})
        yield {"url": response.url}


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                # "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "PLAYWRIGHT_MAX_CONCURRENT_PAGES": 6,
            "CLOSESPIDER_ITEMCOUNT": 40,
        }
    )
    process.crawl(FoolowAllSpider)
    process.start()
