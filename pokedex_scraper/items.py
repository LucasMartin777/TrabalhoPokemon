# pokedex_scraper/items.py

import scrapy

class PokedexScraperItem(scrapy.Item):
    numero = scrapy.Field()
    nome = scrapy.Field()
    url = scrapy.Field()
    evolucoes = scrapy.Field()  # Lista de dicionários com número, nome e URL
    tamanho_cm = scrapy.Field()
    peso_kg = scrapy.Field()
    tipos = scrapy.Field()  # Lista de strings
    habilidades = scrapy.Field()  # Lista de dicionários com URL, nome e descrição
