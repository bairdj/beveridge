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
    return team_mapping[code]

def get_team_code(full_name):
    for code, name in team_mapping.items():
        if name == full_name:
            return code
    return full_name

def get_match_description(response):
    match_container = response.xpath("//td[@colspan = '5' and @align = 'center']")[0]
    match_details = match_container.xpath(".//text()").extract()
    return {
        "round": match_details[1],
        "venue": match_details[3],
        "date": match_details[6],
        "attendance": match_details[8],
        "homeTeam": response.xpath("(//a[contains(@href, 'teams/')])[1]/text()").extract_first(),
        "awayTeam": response.xpath("(//a[contains(@href, 'teams/')])[2]/text()").extract_first(),
        "homeScore": int(response.xpath("//table[1]/tr[2]/td[5]/b/text()").extract_first()),
        "awayScore": int(response.xpath("//table[1]/tr[3]/td[5]/b/text()").extract_first())
    }

def get_match_urls(response):
    for match in response.xpath("//a[contains(@href, 'stats/games/')]/@href").extract():
                yield response.urljoin(match)