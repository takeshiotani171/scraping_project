import os, scrapy, urllib
import time
import random, string

class YahooAuctionsSpider(scrapy.Spider):
    name = 'yahoo_auctions'
   
    allowed_domains = ['auctions.yahoo.co.jp']
    
    start_urls = ['https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=1&oq=%E3%82%B9%E3%83%88%E3%83%A9%E3%83%88%E3%82%AD%E3%83%A3%E3%82%B9%E3%82%BF%E3%83%BC&exflg=1&p=%E3%82%B9%E3%83%88%E3%83%A9%E3%83%88%E3%82%AD%E3%83%A3%E3%82%B9%E3%82%BF%E3%83%BC&x=0&y=0&sc_i=auc_sug_cat',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%AC%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%AB&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=3&oq=%E3%81%A6%E3%82%8C%E3%81%8D%E3%82%83&exflg=1&p=%E3%83%86%E3%83%AC%E3%82%AD%E3%83%A3%E3%82%B9%E3%82%BF%E3%83%BC&sc_i=auc_sug',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%BB%E3%83%9F%E3%82%A2%E3%82%B3&x=29&y=20',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=sg&x=49&y=18',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B8%E3%83%A3%E3%82%AC%E3%83%BC&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=1&oq=%E3%82%B0%E3%83%AC%E3%82%B3&exflg=1&p=%E3%82%B0%E3%83%AC%E3%82%B3&sc_i=auc_sug_cat',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B8%E3%83%A3%E3%82%BA%E3%83%9E%E3%82%B9%E3%82%BF%E3%83%BC&x=26&y=20',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%A2%E3%82%A4%E3%83%90%E3%83%8B%E3%83%BC%E3%82%BA&x=34&y=15',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084046544&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%9E%E3%83%BC%E3%83%81%E3%83%B3&x=20&y=27',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=ARIA&x=27&y=18',
                  'https://auctions.yahoo.co.jp/search/search?va=%E3%82%A2%E3%83%AA%E3%82%A2%E3%83%97%E3%83%AD&exflg=1&b=1&n=50&auccat=2084019019&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%A2%E3%83%AA%E3%82%A2%E3%83%97%E3%83%AD&x=14&y=23',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084046544&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%A4%E3%83%9E%E3%83%8F&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019034&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B0%E3%83%AC%E3%82%B3&x=23&y=9',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019034&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%97%E3%83%AC%E3%82%B8%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%99%E3%83%BC%E3%82%B9&x=35&y=31',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019034&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B8%E3%83%A3%E3%82%BA%E3%83%99%E3%83%BC%E3%82%B9&x=38&y=17',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019034&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%B8%E3%83%83%E3%82%AF%E3%83%9E%E3%83%B3&x=43&y=34',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019034&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%A2%E3%82%A4%E3%83%90%E3%83%8B%E3%83%BC%E3%82%BA&x=45&y=36',
                  'https://auctions.yahoo.co.jp/search/search?auccat=2084019034&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B0%E3%83%AC%E3%82%B3&x=34&y=22',
                  'https://auctions.yahoo.co.jp/search/search?auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&fr=auc_top&p=%E3%82%A8%E3%83%95%E3%82%A7%E3%82%AF%E3%82%BF%E3%83%BC&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%81%E3%83%A5%E3%83%BC%E3%83%8A%E3%83%BC&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=22436&tab_ex=commerce&ei=utf-8&aq=2&oq=%E3%82%A2%E3%83%B3%E3%83%97&exflg=1&p=%E3%82%A2%E3%83%B3%E3%83%97&sc_i=auc_sug_cat',
                  'https://auctions.yahoo.co.jp/search/search?va=%E3%82%AE%E3%82%BF%E3%83%BC%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB&exflg=1&b=1&n=50&auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B9%E3%83%94%E3%83%BC%E3%82%AB%E3%83%BC&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=1&oq=%E3%83%89%E3%83%A9%E3%83%A0&exflg=1&p=%E3%83%89%E3%83%A9%E3%83%A0&x=0&y=0&sc_i=auc_sug_cat',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B5%E3%83%83%E3%82%AF%E3%82%B9&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=MTR&x=37&y=29',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%98%E3%83%83%E3%83%89%E3%83%95%E3%82%A9%E3%83%B3&x=10&y=24',
                  'https://auctions.yahoo.co.jp/search/search?exflg=1&b=1&n=50&s1=featured&auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%83%9A%E3%83%80%E3%83%AB&x=20&y=13',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B7%E3%83%B3%E3%83%90%E3%83%AB&x=51&y=26',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E6%A5%BD%E8%AD%9C&x=20&y=20',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E8%BB%8A&x=35&y=24',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%81%8A%E8%8F%93%E5%AD%90&x=37&y=17',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%B8%E3%83%A5%E3%83%BC%E3%82%B9&x=17&y=20',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E5%AE%B6%E9%9B%BB&x=37&y=35',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24242&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=%E3%82%AA%E3%83%BC%E3%83%87%E3%82%A3%E3%82%AA&x=32&y=36',
                  'https://auctions.yahoo.co.jp/search/search?auccat=24698&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&p=%E3%82%AD%E3%83%A3%E3%83%B3%E3%83%97&x=0&y=0',
                  'https://auctions.yahoo.co.jp/search/search?auccat=26308&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&p=bmw&x=33&y=15']
   
    start_urls = ['https://auctions.yahoo.co.jp/search/search?auccat=22436&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&p=%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89&x=26&y=21']

    
    def parse(self, response):
        number_of_strings = 5
        length_of_string = 8
        for x in range(number_of_strings):
            rand_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

        category = response.css('span.SearchCondition__text::text').extract()[1][5:]
        if category == 'エレキベース本体' or category == '本体':
            label = "guitar"
        else:
            label = "others"

        for i,image in enumerate(response.css('ul.Products__items img')):

            image_url = image.css('::attr(src)').extract_first().strip()

            file_name = f"{rand_str}-{i + 1}.jpg"

            if i < 40:
                self.dest_dir = f'/Users/takeshiotani/Desktop/sagemaker_project/Scrapy_1/yahoo_2/train_data_test/{label}'
            else:
                self.dest_dir = f'/Users/takeshiotani/Desktop/sagemaker_project/Scrapy_1/yahoo_2/verification_data_test/{label}'
    
            if not os.path.exists(self.dest_dir):
                    os.mkdir(self.dest_dir)

            urllib.request.urlretrieve(image_url, os.path.join(self.dest_dir, file_name))

            time.sleep(1)