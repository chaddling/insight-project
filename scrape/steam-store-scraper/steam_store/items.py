# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, MapCompose

def str_to_int(x):
    try:
        return int(float(x))
    except:
        return x


class StripText:
	# strips escaped chars 
    def __init__(self, chars=' \r\t\n-'):
        self.chars = chars

	# making an instance callable!
    def __call__(self, value): 
        try:
            return value.strip(self.chars)
        except:
            return value

class SteamStoreItem(scrapy.Item):

    game_id = scrapy.Field()
    game_name = scrapy.Field()  

	# there are two review fields (recent and overall)
	# under the game_review_summary css element
	# Compose() combines parsing and taking the last element (representing the overall rating)
    p_reviews = scrapy.Field(
        output_processor=Compose(
            MapCompose(
                StripText()
            ),
            lambda x : x[-1] # this will take the last element
        )
    )

    sentiment = scrapy.Field()

class SteamItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
