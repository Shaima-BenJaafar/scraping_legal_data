import string
import scrapy
import pymongo

class HTMLSpider(scrapy.Spider):

    name = 'content_lois_cod_ca'
    start_urls = [f'https://laws-lois.justice.gc.ca/fra/lois/{letter}.html' for letter in string.ascii_uppercase]

    def __init__(self, *args, **kwargs):
        super(HTMLSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['bd_lois']  

    def closed(self, reason):
        self.client.close()

    def parse(self, response):
        for loi in response.css('.TocTitle'):
            url = response.urljoin(loi.css('::attr(href)').get())
            url = url.replace("/index.html", "/TexteComplet.html")
            yield scrapy.Request(url, callback=self.parse_texte_complet,
                                 meta={'url': url})


    def parse_texte_complet(self, response):
        html_title = response.css('h2.Title-of-Act ::text').get()
        doc_contents_text = response.css('div.docContents ::text').getall()
        complete_content = ' '.join(doc_contents_text).strip()

        self.db['lois_codifiées_ca'].insert_one({
            'url': response.meta['url'],
            'id_loi': html_title,
            'content': complete_content,
        })