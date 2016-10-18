import scrapy
from afltables.items import Match
from afltables.loaders import MatchLoader
from afltables.common import get_match_urls

class SeasonSpider(scrapy.Spider):
    name = "season"

    def start_requests(self):
        yield scrapy.Request(url="http://afltables.com/afl/seas/2016.html", callback=self.parse)

    def parse(self, response):
        # get match URLs
        for match in get_match_urls(response):
            yield scrapy.Request(match, callback=self.parse_match)

    def parse_match(self, response):
        match_loader = MatchLoader(selector=response)
        # get top stats (round, venue, date, attendance)
        match_container = response.xpath("//td[@colspan = '5' and @align = 'center']")[0]
        match_details = match_container.xpath(".//text()").extract()
        match_loader.add_value("round", match_details[1])
        match_loader.add_value("venue", match_details[3])
        match_loader.add_value("date", match_details[6])
        match_loader.add_value("attendance", match_details[8])
        match_loader.add_xpath("homeTeam", "(//a[contains(@href, 'teams/')])[1]/text()")
        match_loader.add_xpath("awayTeam", "(//a[contains(@href, 'teams/')])[2]/text()")

        return match_loader.load_item()
