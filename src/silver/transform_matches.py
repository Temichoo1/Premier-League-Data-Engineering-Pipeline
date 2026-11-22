def flatten_match(match):

    flattened_match = {
        "MatchID": match["match_id"],
        "MatchDate": match["match_date"],
        "DateUnix": match["date_unix"],
        "MatchStatus": match["status"],
        "MatchStatusLocalized": match["status_localized"],
        "RoundID": match["round_id"],
        "GameWeek": match["game_week"],

        "LeagueID": match["league"]["league_id"],
        "LeagueName": match["league"]["name"],
        "Country": match["league"]["country"],
        "CompetitionName": match["league"]["competition_name"],
        "LeagueImage": match["league"]["league_image"],

        "SeasonID": match["season"]["season_id"],
        "SeasonYear": match["season"]["year"],

        "HomeTeamID": match["home_team"]["team_id"],
        "HomeTeamName": match["home_team"]["team_name"],
        "HomeTeamLogo": match["home_team"]["team_logo"],

        "AwayTeamID": match["away_team"]["team_id"],
        "AwayTeamName": match["away_team"]["team_name"],
        "AwayTeamLogo": match["away_team"]["team_logo"],

        "HomeGoals": match["score"]["home"],
        "AwayGoals": match["score"]["away"],
        "SourceTotalGoals": match["score"]["total_goals"],

        "HomeXG": match["xg"]["home"],
        "AwayXG": match["xg"]["away"],
        "TotalXG": match["xg"]["total"],

        "HomeWinOdds": match["odds"]["home_win"],
        "DrawOdds": match["odds"]["draw"],
        "AwayWinOdds": match["odds"]["away_win"],

        "HomeWinProbability": match["probabilities"]["home_win"],
        "DrawProbability": match["probabilities"]["draw"],
        "AwayWinProbability": match["probabilities"]["away_win"],

        "StadiumName": match["venue"]["stadium_name"],
        "StadiumLocation": match["venue"]["stadium_location"],

        "LastUpdated": match["last_updated"],
        "WinnerText": match["winner_text"]
    }

    return flattened_match