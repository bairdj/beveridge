# -*- coding: utf-8 -*-
import scrapy
from afltables.common import get_match_urls, get_team_code, get_match_description
from afltables.items import TeamStats

class StatsSpider(scrapy.Spider):
    name = "stats"

    start_urls = []

    def __init__(self, start_season=None, end_season=None, *args, **kwargs):
        super(StatsSpider, self).__init__(*args, **kwargs)
        if start_season is None:
            start_season = 2015
        if end_season is None:
            end_season = 2017
        seasons = range(int(start_season), int(end_season) + 1)
        for season in seasons:
            self.start_urls.append("http://afltables.com/afl/seas/{:d}.html".format(season))


    def parse(self, response):
        for match in get_match_urls(response):
            yield scrapy.Request(match, callback=self.parse_stats)

    def parse_team(self, table):
        team = TeamStats()
        # if there's 3 rows the first row is rushed behinds
        row_count = len(table.xpath(".//tr"))
        stats = table.xpath(".//tr[{:d}]".format(row_count-1))
        opposition_stats = table.xpath(".//tr[{:d}]".format(row_count))
        #reuse xpath template
        td_xpath = "normalize-space(.//td[{:d}])"
        team["kicks"] = stats.xpath(td_xpath.format(2)).extract_first()
        team["oppKicks"] = opposition_stats.xpath(td_xpath.format(2)).extract_first()
        team["marks"] = stats.xpath(td_xpath.format(3)).extract_first()
        team["oppMarks"] = opposition_stats.xpath("normalize-space(.//td[3])").extract_first()
        team["handballs"] = stats.xpath("normalize-space(.//td[4])").extract_first()
        team["oppHandballs"] = opposition_stats.xpath("normalize-space(.//td[4])").extract_first()
        team["disposals"] = stats.xpath("normalize-space(.//td[5])").extract_first()
        team["oppDisposals"] = opposition_stats.xpath("normalize-space(.//td[5])").extract_first()
        team["hitouts"] = stats.xpath("normalize-space(.//td[8])").extract_first()
        team["oppHitouts"] = opposition_stats.xpath("normalize-space(.//td[8])").extract_first()
        team["tackles"] = stats.xpath("normalize-space(.//td[9])").extract_first()
        team["oppTackles"] = opposition_stats.xpath("normalize-space(.//td[9])").extract_first()
        team["rebounds"] = stats.xpath("normalize-space(.//td[10])").extract_first()
        team["oppRebounds"] = opposition_stats.xpath("normalize-space(.//td[10])").extract_first()
        # TODO finish the rest of the columns
        return team

    def parse_stats(self, response):
        # get round
        round = int(response.xpath("/html/body/center/table[1]/tr[1]/td[2]/text()[1]").extract_first())
        match_details = get_match_description(response)
        # get home team first. id = sortableTable0
        home_team = self.parse_team(response.css(".sortable tfoot")[0])
        home_team["team"] = get_team_code(response.xpath("(//a[contains(@href, 'teams/')])[1]/text()").extract_first())
        home_team["round"] = round
        home_team["score"] = match_details["homeScore"]
        home_team["oppScore"] = match_details["awayScore"]
        home_team["win"] = match_details["homeScore"] > match_details["awayScore"]
        home_team["home"] = True
        yield home_team
        # get away team. id = sortableTable1
        away_team = self.parse_team(response.css(".sortable tfoot")[1])
        away_team["team"] = get_team_code(response.xpath("(//a[contains(@href, 'teams/')])[2]/text()").extract_first())
        away_team["round"] = round
        away_team["win"] = match_details["awayScore"] > match_details["homeScore"]
        away_team["home"] = False
        away_team["score"] = match_details["awayScore"]
        away_team["oppScore"] = match_details["homeScore"]
        yield away_team
