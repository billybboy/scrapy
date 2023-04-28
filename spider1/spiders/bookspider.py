import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            yield{
                'name' : book.css('h3 a::text').get(),
                'price' : book.css('.product_price .price_color::text').get(),
                'url' : book.css('h3 a::attr(href)').get(), # 也可以寫成book.css('h3 a').attr['href]
            }
        # 往下一頁繼續爬
        next_page = response.css('li.next a::attr(href)').get()

        if next_page:
            # 因網站的每頁next按鍵html不完全相同，故用if else讓每頁都能爬到
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)
#get()會回傳第一個response的所有內含html