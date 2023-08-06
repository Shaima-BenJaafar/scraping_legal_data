# data_juridique



## Getting started

Le projet de Collecte Complète des Lois du Canada et du Québec vise à rassembler, compiler et mettre à disposition une base de données exhaustive de toutes les lois et régulations en vigueur au niveau fédéral et provincial dans les juridictions canadiennes.

Ce projet vise à collecter des données depuis deux liens web spécifiques en utilisant Scrapy, un framework de scraping en Python.

les deux liens :

https://www.legisquebec.gouv.qc.ca/fr/chapitres?corpus=lois

https://laws-lois.justice.gc.ca/fra/lois/

##  How to run?
Assurez-vous d'avoir Python 3 installé. Pour installer les dépendances nécessaires, vous pouvez utiliser pip :

pip install scrapy
pip install pymongo

Vous avez en disposition 6 script :

Pour avoir les Lois codifiées du canada : scrapy crawl content_lois_cod_ca

Pour avoir les Règlements codifiés du canada : scrapy crawl content_reg_ca

Pour avoir les lois annuelles du canada : scrapy crawl content_lois_a_ca

Pour avoir les LOIS CONSTITUTIONNELLES DE 1867 à 1982 du canada : scrapy crawl content_txt_const_ca

Pour avoir les Lois codifiées du quebec : scrapy crawl content_lois_qb

Pour avoir les Règlements codifiés du quebec : scrapy crawl content_reg_qb
