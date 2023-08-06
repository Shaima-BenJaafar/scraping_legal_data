import re
import scrapy
import pymongo

class HTMLSpider(scrapy.Spider):

    name = 'content_lois_a_ca'
    start_urls = [f'https://laws-lois.justice.gc.ca/fra/LoisAnnuelles/index{i}.html' for i in range(2001, 2024)]

    def __init__(self, *args, **kwargs):
        super(HTMLSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['bd_lois']  

    def closed(self, reason):
        self.client.close()

    def parse(self, response):
        for loi in response.css('.annualLeft'):
            url = response.urljoin(loi.css('a ::attr(href)').get())
            html_title = loi.css('a ::text').get()
            yield scrapy.Request(f'{url}/TexteComplet.html', callback=self.parse_texte_complet, meta={'url': url, 'html_title': html_title})

    def parse_texte_complet(self, response):
        doc_contents_text = response.css('div.docContents ::text').getall()
        complete_content = ' '.join(doc_contents_text).strip()

        self.db['lois_annuelles_ca'].insert_one({
            'url': response.meta['url'],
            'id_lois_a': response.meta['html_title'],
            'content': complete_content,
        })


