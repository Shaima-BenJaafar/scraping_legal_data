import pymongo
import scrapy


class HTMLSpider(scrapy.Spider):
    name = 'content_reg_qb'
    start_urls = ['https://www.legisquebec.gouv.qc.ca/fr/chapitres?corpus=regs&selection=tout']

    def __init__(self, *args, **kwargs):
        super(HTMLSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['bd_lois']

    def closed(self, reason):
        self.client.close()

    def parse(self, response):
        for loi in response.css('.clickable'):
            url = response.urljoin(loi.css('a ::attr(href)').get())
            loi_id = loi.css('th ::text').get()
            loi_id = loi_id.split(',')[0].strip()
            titre_reglement = loi.css('a ::attr(title)').get()
            yield scrapy.Request(url, callback=self.parse_texte_complet_reg,
                                 meta={'url': url,'loi_id': loi_id, 'titre_reglement':titre_reglement})



    def parse_texte_complet_reg(self, response):
        doc_contents_text = response.css('div.card-body.history.current.conso ::text').getall()

        if not doc_contents_text:
            doc_contents_text = response.css('div.card-body.history.current.rep ::text').getall()

        complete_content = ' '.join(doc_contents_text).strip()

        self.db['reglements_codifiées_qb'].insert_one({
            'url': response.meta['url'],
            'id_loi': response.meta['loi_id'],
            'id_reglement': response.meta['titre_reglement'],
            'content': complete_content,
        })

