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
        matchLoader = MatchLoader(selector=response)
        # get top stats (round, venue, date, attendance)
        matchContainer = response.xpath("//td[@colspan = '5' and @align = 'center']")[0]
        matchDetails = matchContainer.xpath(".//text()").extract()
        matchLoader.add_value("round", matchDetails[1])
        matchLoader.add_value("venue", matchDetails[3])
        matchLoader.add_value("date", matchDetails[6])
        matchLoader.add_value("attendance", matchDetails[8])
        matchLoader.add_xpath("homeTeam", "(//a[contains(@href, 'teams/')])[1]/text()")
        matchLoader.add_xpath("awayTeam", "(//a[contains(@href, 'teams/')])[2]/text()")
        homeScores = matchLoader.nested_xpath("/html/body/center/table[1]//tr[2]")

        return matchLoader.load_item()
