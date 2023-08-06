import string
import scrapy
import pymongo

class HTMLSpider(scrapy.Spider):

    name = 'content_reg_ca'
    start_urls = [f'https://laws-lois.justice.gc.ca/fra/reglements/{letter}.html' for letter in string.ascii_uppercase]

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
        loi_titles =[]
        for loi in response.css('p.EnablingAct'):
            loi_title = loi.css("::text").get()
            loi_titles.append(loi_title)

        loi_titles = [act.strip().lower().capitalize() for act in loi_titles]
        loi_titles = ', '.join(loi_titles).strip()
        doc_contents_text = response.css('div.docContents ::text').getall()
        complete_content = ' '.join(doc_contents_text).strip()

        self.db['règlements_codifiés_ca'].insert_one({
            'url': response.meta['url'],
            'id_reglement': html_title,
            'id_loi': loi_titles,
            'content': complete_content,
        })