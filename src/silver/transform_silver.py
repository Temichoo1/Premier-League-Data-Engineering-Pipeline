def build_silver_datasets(flattened_matches):

    leagues = []
    seasons = []
    teams = []
    venues = []
    matches = []
    match_scores = []
    match_statistics = []

    for match in flattened_matches:

        # 1. Leagues
        leagues.append({
            "LeagueID": match["LeagueID"],
            "LeagueName": match["LeagueName"],
            "Country": match["Country"],
            "CompetitionName": match["CompetitionName"],
            "LeagueImage": match["LeagueImage"]
        })

        # 2. Seasons
        seasons.append({
            "SeasonID": match["SeasonID"],
            "SeasonYear": match["SeasonYear"],
            "LeagueID": match["LeagueID"]
        })

        # 3. Teams
        teams.append({
            "TeamID": match["HomeTeamID"],
            "TeamName": match["HomeTeamName"],
            "TeamLogo": match["HomeTeamLogo"]
        })

        teams.append({
            "TeamID": match["AwayTeamID"],
            "TeamName": match["AwayTeamName"],
            "TeamLogo": match["AwayTeamLogo"]
        })

        # 4. Venues
        venues.append({
            "StadiumName": match["StadiumName"],
            "StadiumLocation": match["StadiumLocation"]
        })

        # 5. Matches
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
            "StadiumName": match["StadiumName"],
            "StadiumLocation": match["StadiumLocation"],
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
        "Leagues": leagues,
        "Seasons": seasons,
        "Teams": teams,
        "Venues": venues,
        "Matches": matches,
        "MatchScores": match_scores,
        "MatchStatistics": match_statistics
    }