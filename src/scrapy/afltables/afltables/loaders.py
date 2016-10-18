from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import TakeFirst
from afltables.items import Match

class MatchLoader(ItemLoader):
    default_item_class = Match
    default_input_processor = MapCompose(lambda i: i.strip())
    default_output_processor = TakeFirst()