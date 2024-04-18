import scrapy
import json
import datetime


class OlxHouses(scrapy.Spider):
    name = 'olx'

    date = datetime.datetime.now().strftime("%Y%m%d")


    custom_settings = {
        'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'AUTOTHROTTLE_ENABLED': True,
        'FEED_URI': f'olx_results_{date}.json',
        'FEED_FORMAT': 'json',
    }
 
    def start_requests(self):
        for page in range(1,101):
            yield scrapy.Request(f'https://www.olx.com.br/imoveis/venda/estado-pr/regiao-de-curitiba-e-paranagua?o={page}')
 

    def parse_house(self, response):
        script_data = response.xpath('//script[@type="application/ld+json"]/text()').get()

        if script_data is not None:
            data = json.loads(script_data)          

            yield{
                'name' : data["Object"]["name"],
                'description' : data["Object"]["description"],
                'url' : data["Object"]["url"]
            }

    def parse(self, response, **kwargs):
        html = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').get())

        houses = html.get('props').get('pageProps').get('ads')
        for house in houses:
            url = house.get('url')
            if isinstance(url, str):
                yield scrapy.Request(url, callback=self.parse_house)        
        