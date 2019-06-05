import scrapy
from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import SteamStoreItem, SteamItemLoader

# scrape a game's rating through the Steam web page
class SteamSpider(Spider):

    name = 'steam-spider'

    def __init__(self, filename=None):
        if filename:
            with open(filename, 'r') as f:
                self.start_urls = [url.strip() for url in f.readlines()]

    def parse(self, response):
		# loader object 
        loader = SteamItemLoader(item=SteamStoreItem(), response=response)

        current_id = response.request.url

        loader.add_value('game_id', int(current_id.split('/')[-2]))

		# looks for corresponding css elements and extract the text values
        loader.add_css('game_name', '.apphub_AppName ::text') 
        loader.add_css('p_reviews', '.responsive_reviewdesc::text')
        loader.add_css('sentiment', '.game_review_summary::text')
        return loader.load_item()
