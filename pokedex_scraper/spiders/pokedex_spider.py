# pokedex_scraper/spiders/pokedex_spider.py

import scrapy
from pokedex_scraper.items import PokedexScraperItem
from urllib.parse import urljoin

class PokedexSpider(scrapy.Spider):
    name = "pokedex"
    allowed_domains = ["pokemondb.net"]
    start_urls = ["https://pokemondb.net/pokedex/all"]

    def parse(self, response):
        rows = response.xpath('//table[contains(@id, "pokedex")]/tbody/tr')
        for row in rows:
            item = PokedexScraperItem()
            # Número
            item['numero'] = row.xpath('.//td[@class="cell-num"]/text()').get().strip('# ')
            nome_cell = row.xpath('.//td[@class="cell-name"]')
            item['nome'] = nome_cell.xpath('.//a/text()').get()
            relative_url = nome_cell.xpath('.//a/@href').get()
            item['url'] = urljoin(response.url, relative_url)
            tipos = row.xpath('.//td[@class="cell-icon"]/a/text()').getall()
            item['tipos'] = [tipo.strip() for tipo in tipos]
            peso_tamanho = row.xpath('.//td[@class="cell-pokemon"]/text()').getall()
            if peso_tamanho:
                peso_kg_text = row.xpath('.//td[@class="cell-pokemon"]/text()').re_first(r'\(([\d.]+) kg\)')
                item['peso_kg'] = float(peso_kg_text) if peso_kg_text else None
            else:
                item['peso_kg'] = None
            item['evolucoes'] = []
            item['habilidades'] = []
            yield scrapy.Request(
                url=item['url'],
                callback=self.parse_pokemon,
                meta={'item': item}
            )

    def parse_pokemon(self, response):
        item = response.meta['item']
        tamanho_text = response.xpath('//th[text()="Height"]/following-sibling::td/text()').get()
        if tamanho_text:
            tamanho_cm = None
            height_match = response.xpath('//th[text()="Height"]/following-sibling::td/text()').re_first(r'([\d.]+)\s*m')
            if height_match:
                tamanho_cm = float(height_match) * 100  # metros para cm
            item['tamanho_cm'] = tamanho_cm
        else:
            item['tamanho_cm'] = None
        # Evoluções
        evolucoes = []
        evol_section = response.xpath('//span[text()="Evolution"]/ancestor::h2/following-sibling::div')
        if evol_section:
            evol_rows = evol_section.xpath('.//table//tr')
            for evol in evol_rows:
                numero = evol.xpath('.//td[1]/text()').get()
                nome = evol.xpath('.//td[2]/a/text()').get()
                relative_evol_url = evol.xpath('.//td[2]/a/@href').get()
                evol_url = urljoin(response.url, relative_evol_url)
                evolucoes.append({
                    'numero': numero,
                    'nome': nome,
                    'url': evol_url
                })
        item['evolucoes'] = evolucoes
        habilidades = []
        habilidades_section = response.xpath('//span[text()="Abilities"]/ancestor::h2/following-sibling::div')
        if habilidades_section:
            habilidade_rows = habilidades_section.xpath('.//table//tr')
            for hab in habilidade_rows:
                nome = hab.xpath('.//td[1]/a/text()').get()
                relative_hab_url = hab.xpath('.//td[1]/a/@href').get()
                hab_url = urljoin(response.url, relative_hab_url)
                yield scrapy.Request(
                    url=hab_url,
                    callback=self.parse_habilidade,
                    meta={'item': item, 'habilidade_nome': nome}
                )
        else:
            item['habilidades'] = habilidades
            yield item  

    def parse_habilidade(self, response):
        item = response.meta['item']
        nome = response.meta['habilidade_nome']
        descricao = response.xpath('//div[@class="grid-col span-md-6"]/p/text()').get()
        habilidades = item.get('habilidades', [])
        habilidades.append({
            'nome': nome,
            'url': response.url,
            'descricao': descricao.strip() if descricao else None
        })
        item['habilidades'] = habilidades
        yield item
