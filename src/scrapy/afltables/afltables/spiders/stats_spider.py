# -*- coding: utf-8 -*-
import scrapy
from afltables.common import get_match_urls, get_team_code, get_match_description
from afltables.items import TeamStats

class StatsSpider(scrapy.Spider):
    name = "stats"

    start_urls = []

    def __init__(self, startSeason=None, endSeason=None, *args, **kwargs):
        super(StatsSpider, self).__init__(*args, **kwargs)
        if startSeason == None:
            startSeason = 2015
        if endSeason == None:
            endSeason = 2017
        seasons = range(int(startSeason),int(endSeason)+1)
        for season in seasons:
            self.start_urls.append("http://afltables.com/afl/seas/{:d}.html".format(season))


    def parse(self, response):
        for match in get_match_urls(response):
            yield scrapy.Request(match, callback=self.parse_stats)

    def parse_team(self, table, homeTeam):
        team = TeamStats()
        # if there's 3 rows the first row is rushed behinds
        rowCount = len(table.xpath(".//tr"))
        stats = table.xpath(".//tr[{:d}]".format(rowCount-1))
        oppositionStats = table.xpath(".//tr[{:d}]".format(rowCount))
        #reuse xpath template
        td_xpath = "normalize-space(.//td[{:d}])"
        team["kicks"] = stats.xpath(td_xpath.format(2)).extract_first()
        team["oppKicks"] = oppositionStats.xpath(td_xpath.format(2)).extract_first()
        team["marks"] = stats.xpath(td_xpath.format(3)).extract_first()
        team["oppMarks"] = oppositionStats.xpath("normalize-space(.//td[3])").extract_first()
        team["handballs"] = stats.xpath("normalize-space(.//td[4])").extract_first()
        team["oppHandballs"] = oppositionStats.xpath("normalize-space(.//td[4])").extract_first()
        team["disposals"] = stats.xpath("normalize-space(.//td[5])").extract_first()
        team["oppDisposals"] = oppositionStats.xpath("normalize-space(.//td[5])").extract_first()
        team["hitouts"] = stats.xpath("normalize-space(.//td[8])").extract_first()
        team["oppHitouts"] = oppositionStats.xpath("normalize-space(.//td[8])").extract_first()
        team["tackles"] = stats.xpath("normalize-space(.//td[9])").extract_first()
        team["oppTackles"] = oppositionStats.xpath("normalize-space(.//td[9])").extract_first()
        team["rebounds"] = stats.xpath("normalize-space(.//td[10])").extract_first()
        team["oppRebounds"] = oppositionStats.xpath("normalize-space(.//td[10])").extract_first()
        # TODO finish the rest of the columns
        return team

    def parse_stats(self, response):
        # get round
        round = int(response.xpath("/html/body/center/table[1]/tr[1]/td[2]/text()[1]").extract_first())
        matchDetails = get_match_description(response)
        # get home team first. id = sortableTable0
        homeTeam = self.parse_team(response.css(".sortable tfoot")[0], True)
        homeTeam["team"] = get_team_code(response.xpath("(//a[contains(@href, 'teams/')])[1]/text()").extract_first())
        homeTeam["round"] = round
        homeTeam["score"] = matchDetails["homeScore"]
        homeTeam["oppScore"] = matchDetails["awayScore"]
        homeTeam["win"] = matchDetails["homeScore"] > matchDetails["awayScore"]
        homeTeam["home"] = True
        yield homeTeam
        # get away team. id = sortableTable1
        awayTeam = self.parse_team(response.css(".sortable tfoot")[1], False)
        awayTeam["team"] = get_team_code(response.xpath("(//a[contains(@href, 'teams/')])[2]/text()").extract_first())
        awayTeam["round"] = round
        awayTeam["win"] = matchDetails["awayScore"] > matchDetails["homeScore"]
        awayTeam["home"] = False
        awayTeam["score"] = matchDetails["awayScore"]
        awayTeam["oppScore"] = matchDetails["homeScore"]
        yield awayTeam
