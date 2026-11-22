def build_silver_datasets(flattened_matches):

    leagues = {}
    seasons = {}
    teams = {}
    venues = {}
    venue_lookup = {}
    matches = []
    match_scores = []
    match_statistics = []
   

    for match in flattened_matches:

       # 1. Leagues
        leagues[match["LeagueID"]] = {
            "LeagueID": match["LeagueID"],
            "LeagueName": match["LeagueName"],
            "Country": match["Country"],
            "CompetitionName": match["CompetitionName"],
            "LeagueImage": match["LeagueImage"]
        }

        # 2. Seasons
        seasons[match["SeasonID"]] = {
            "SeasonID": match["SeasonID"],
            "SeasonYear": match["SeasonYear"],
            "LeagueID": match["LeagueID"]
        }

        # 3. Teams
        teams[match["AwayTeamID"]] = {
            "TeamID": match["AwayTeamID"],
            "TeamName": match["AwayTeamName"],
            "TeamLogo": match["AwayTeamLogo"]
        }


        # 4. Venues

        stadium_name = match["StadiumName"]
        stadium_location = match["StadiumLocation"]

        # Clean venue data
        if stadium_name:
            stadium_name = stadium_name.strip()

        if stadium_location:
            stadium_location = stadium_location.strip()

        # Only process venues with a stadium name
        if stadium_name:

            venue_key = (stadium_name, stadium_location)

            # Generate a VenueID for new venues
            if venue_key not in venue_lookup:

                venue_id = len(venue_lookup) + 1

                venue_lookup[venue_key] = venue_id

                venues[venue_key] = {
                    "VenueID": venue_id,
                    "StadiumName": stadium_name,
                    "StadiumLocation": stadium_location
                }

        # 5. Matches

        match_venue_id = None

        if stadium_name:
            venue_key = (stadium_name, stadium_location)
            match_venue_id = venue_lookup.get(venue_key)

        matches.append({
            "MatchID": match["MatchID"],
            "MatchDate": match["MatchDate"],
            "DateUnix": match["DateUnix"],
            "MatchStatus": match["MatchStatus"],
            "MatchStatusLocalized": match["MatchStatusLocalized"],
            "RoundID": match["RoundID"],
            "GameWeek": match["GameWeek"],
            "SeasonID": match["SeasonID"],
            "HomeTeamID": match["HomeTeamID"],
            "AwayTeamID": match["AwayTeamID"],
            "VenueID": match_venue_id,
            "LastUpdated": match["LastUpdated"],
            "WinnerText": match["WinnerText"]
         })

        # 6. Match scores
        calculated_total_goals = match["HomeGoals"] + match["AwayGoals"]

        match_scores.append({
            "MatchID": match["MatchID"],
            "HomeGoals": match["HomeGoals"],
            "AwayGoals": match["AwayGoals"],
            "SourceTotalGoals": match["SourceTotalGoals"],
            "CalculatedTotalGoals": calculated_total_goals,
            "IsScoreValid": match["SourceTotalGoals"] == calculated_total_goals
        })

        # 7. Match statistics
        match_statistics.append({
            "MatchID": match["MatchID"],
            "HomeXG": match["HomeXG"],
            "AwayXG": match["AwayXG"],
            "TotalXG": match["TotalXG"],
            "HomeWinOdds": match["HomeWinOdds"],
            "DrawOdds": match["DrawOdds"],
            "AwayWinOdds": match["AwayWinOdds"],
            "HomeWinProbability": match["HomeWinProbability"],
            "DrawProbability": match["DrawProbability"],
            "AwayWinProbability": match["AwayWinProbability"]
        })

    return {
        "Leagues": list(leagues.values()),
        "Seasons": list(seasons.values()),
        "Teams": list(teams.values()),
        "Venues": list(venues.values()),
        "Matches": matches,
        "MatchScores": match_scores,
        "MatchStatistics": match_statistics
    }