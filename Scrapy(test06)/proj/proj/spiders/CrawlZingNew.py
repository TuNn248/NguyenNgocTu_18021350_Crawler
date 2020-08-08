import scrapy
import json

output_filename = "D:\PycharmProjects\Scrapy(test06)\proj\proj\spiders\output\pageInfo.txt"

class Crawler(scrapy.Spider):
    name = "czn"
    start_urls = ["https://zingnews.vn/"]
    Crawled_Count = 0

    def parse(self, response):
        if response.status == 200 and response.css('meta[property="og:type"]::attr(content)').get() == "article":
            print("Crawling from: ", response.url)
            data = {
                "link: ": response.url,
                "title: ": response.css("h1.the-article-title::text").get(),
                "des: ": response.css("p.the-article-summary::text").get(),
                "published_time: ": response.css('meta[property="article:published_time"]::attr(content)').get(),
                "tags: ": [
                    t.strip() for t in response.css('meta[property="article:tag"]::attr(content)').get().split(',')
                ]
            }

            with open(output_filename, "a", encoding="utf-8") as f:
                f.write(json.dump(data, ensure_ascii=False))
                f.write("\n")
                self.Crawled_Count += 1
                self.crawler.stats.set_value("Crawled_Count", self.Crawled_Count)
                print("success")
        yield from response.follow_all(css = 'a[href^="https://zingnews.vn"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)
