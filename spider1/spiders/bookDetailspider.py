import scrapy
from spider1.items import BookItem

class BookdetailspiderSpider(scrapy.Spider):
    name = "bookDetailspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        
        for book in books:
            # 進入book細節的相對連結
            relatve_url = book.css('h3 a::attr(href)').get()

            if 'catalogue/' in relatve_url:
                book_url = 'https://books.toscrape.com/' + relatve_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relatve_url
            # 將相對連結加入網站後進行parse_bool_page
            yield response.follow(book_url, callback = self.parse_book_page)


        # 往下一頁
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            # 因網站的每頁next按鍵html不完全相同，故用if else讓每頁都能爬到
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)
    

    def parse_book_page(self, response):
        # 對每本書的細節進行爬蟲
        table_rows = response.css('table tr')
        book_item = BookItem()


        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css('td::text').get(),
        book_item['type'] = table_rows[1].css('td::text').get(), # 因為已經變成list所以index從0開始
        book_item['price_excl_tax'] = table_rows[2].css('td::text').get(),
        book_item['price_incl_tax'] = table_rows[3].css('td::text').get(),
        book_item['tax'] = table_rows[4].css('td::text').get(),
        book_item['availability'] = table_rows[5].css('td::text').get(),
        book_item['num_reviews'] = table_rows[6].css('td::text').get(),
        book_item['stars'] = response.css('p.star-rating').attrib['class'],
        book_item['category'] = response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').get(),
        book_item['description'] = response.xpath('//article[@class="product_page"]/p/text()').get(),
        # 也可以寫成 'description' : response.xpath('//div[@id="product_description"]/following-sibling::p/text()').get()
        book_item['price'] = response.css('p.price_color::text').get(),

        yield book_item
