INSERT INTO Gold.MatchAnalysis
(
    MatchID,
    MatchDate,
    SeasonYear,
    GameWeek,
    HomeTeam,
    AwayTeam,
    HomeGoals,
    AwayGoals,
    TotalGoals,
    MatchResult,
    WinningTeam,
    StadiumName,
    StadiumLocation,
    HomeXG,
    AwayXG,
    TotalXG,
    HomeWinOdds,
    DrawOdds,
    AwayWinOdds,
    HomeWinProbability,
    DrawProbability,
    AwayWinProbability
)
SELECT
    M.MatchID,
    M.MatchDate,
    S.SeasonYear,
    M.GameWeek,

    HT.TeamName AS HomeTeam,
    AT.TeamName AS AwayTeam,

    MS.HomeGoals,
    MS.AwayGoals,
    MS.CalculatedTotalGoals AS TotalGoals,

    CASE
        WHEN MS.HomeGoals > MS.AwayGoals THEN 'H'
        WHEN MS.HomeGoals = MS.AwayGoals THEN 'D'
        WHEN MS.HomeGoals < MS.AwayGoals THEN 'A'
    END AS MatchResult,

    CASE
        WHEN MS.HomeGoals > MS.AwayGoals THEN HT.TeamName
        WHEN MS.AwayGoals > MS.HomeGoals THEN AT.TeamName
        ELSE NULL
    END AS WinningTeam,

    V.StadiumName,
    V.StadiumLocation,

    ST.HomeXG,
    ST.AwayXG,
    ST.TotalXG,

    ST.HomeWinOdds,
    ST.DrawOdds,
    ST.AwayWinOdds,

    ST.HomeWinProbability,
    ST.DrawProbability,
    ST.AwayWinProbability

FROM Silver.Matches M

INNER JOIN Silver.Seasons S
    ON M.SeasonID = S.SeasonID

INNER JOIN Silver.Teams HT
    ON M.HomeTeamID = HT.TeamID

INNER JOIN Silver.Teams AT
    ON M.AwayTeamID = AT.TeamID

LEFT JOIN Silver.Venues V
    ON M.VenueID = V.VenueID

INNER JOIN Silver.MatchScores MS
    ON M.MatchID = MS.MatchID

LEFT JOIN Silver.MatchStatistics ST
    ON M.MatchID = ST.MatchID;