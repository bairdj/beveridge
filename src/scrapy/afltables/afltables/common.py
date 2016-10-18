team_mapping = {
    "SY": "Sydney",
    "WB": "Western Bulldogs",
    "WC": "West Coast",
    "HW": "Hawthorn",
    "GE": "Geelong",
    "FR": "Fremantle",
    "RI": "Richmond",
    "CW": "Collingwood",
    "CA": "Carlton",
    "GW": "Greater Western Sydney",
    "AD": "Adelaide",
    "GC": "Gold Coast",
    "ES": "Essendon",
    "ME": "Melbourne",
    "NM": "North Melbourne",
    "PA": "Port Adelaide",
    "BL": "Brisbane Lions",
    "SK": "St Kilda"
}

def get_team_name(code):
    return team_mapping[full_name]

def get_team_code(full_name):
    for code, name in team_mapping.items():
        if name == full_name:
            return code
    return full_name

def get_match_description(response):
    matchContainer = response.xpath("//td[@colspan = '5' and @align = 'center']")[0]
    matchDetails = matchContainer.xpath(".//text()").extract()
    return {
        "round": matchDetails[1],
        "venue": matchDetails[3],
        "date": matchDetails[6],
        "attendance": matchDetails[8],
        "homeTeam": response.xpath("(//a[contains(@href, 'teams/')])[1]/text()").extract_first(),
        "awayTeam": response.xpath("(//a[contains(@href, 'teams/')])[2]/text()").extract_first(),
        "homeScore": int(response.xpath("//table[1]/tr[2]/td[5]/b/text()").extract_first()),
        "awayScore": int(response.xpath("//table[1]/tr[3]/td[5]/b/text()").extract_first())
    }
    matchLoader.add_value("round", matchDetails[1])
    matchLoader.add_value("venue", matchDetails[3])
    matchLoader.add_value("date", matchDetails[6])
    matchLoader.add_value("attendance", matchDetails[8])

def get_match_urls(response):
    for match in response.xpath("//a[contains(@href, 'stats/games/')]/@href").extract():
                yield response.urljoin(match)