import scrapy
import pymongo

class HTMLSpider(scrapy.Spider):

    name = 'content_txt_const_ca'
    start_urls = ['https://laws-lois.justice.gc.ca/fra/Const//TexteComplet.html']

    def __init__(self, *args, **kwargs):
        super(HTMLSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['bd_lois']  

    def closed(self, reason):
        self.client.close()

    def parse(self, response):
        html_title = response.css('.intro h2::text').get()
        doc_contents_text = response.css('div.docContents ::text').getall()
        complete_content = ' '.join(doc_contents_text).strip()

        self.db['lois_constitutionnelles_de_1867_à_1982_ca'].insert_one({
            'url': response.url,
            'id_loi': html_title,
            'content': complete_content,
        })
