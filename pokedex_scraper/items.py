# pokedex_scraper/items.py

import scrapy

class PokedexScraperItem(scrapy.Item):
    numero = scrapy.Field()
    nome = scrapy.Field()
    url = scrapy.Field()
    evolucoes = scrapy.Field()  
    tamanho_cm = scrapy.Field()
    peso_kg = scrapy.Field()
    tipos = scrapy.Field()  
    habilidades = scrapy.Field()  
