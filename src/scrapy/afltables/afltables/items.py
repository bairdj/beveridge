# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Match(scrapy.Item):
    round = scrapy.Field()
    venue = scrapy.Field()
    date = scrapy.Field()
    attendance = scrapy.Field()
    homeTeam = scrapy.Field()
    awayTeam = scrapy.Field()

class TeamStats(scrapy.Item):
    matchId = scrapy.Field()
    team = scrapy.Field()
    round = scrapy.Field()
    win = scrapy.Field()
    home = scrapy.Field()
    # Absolute fields
    score = scrapy.Field()
    kicks = scrapy.Field()
    marks = scrapy.Field()
    handballs = scrapy.Field()
    disposals = scrapy.Field()
    hitouts = scrapy.Field()
    tackles = scrapy.Field()
    rebounds = scrapy.Field()
    inside50s = scrapy.Field()
    clearances = scrapy.Field()
    clangers = scrapy.Field()
    frees = scrapy.Field()
    contested = scrapy.Field()
    uncontested = scrapy.Field()
    contestedMarks = scrapy.Field()
    marksIn50 = scrapy.Field()
    onePercenters = scrapy.Field()
    bounces = scrapy.Field()
    # Opposition fields
    oppScore = scrapy.Field()
    oppKicks = scrapy.Field()
    oppMarks = scrapy.Field()
    oppHandballs = scrapy.Field()
    oppDisposals = scrapy.Field()
    oppHitouts = scrapy.Field()
    oppTackles = scrapy.Field()
    oppRebounds = scrapy.Field()
    oppInside50s = scrapy.Field()
    oppClearances = scrapy.Field()
    oppClangers = scrapy.Field()
    oppFrees = scrapy.Field()
    oppContested = scrapy.Field()
    oppUncontested = scrapy.Field()
    oppContestedMarks = scrapy.Field()
    oppMarksIn50 = scrapy.Field()
    oppOnePercenters = scrapy.Field()
    oppBounces = scrapy.Field()