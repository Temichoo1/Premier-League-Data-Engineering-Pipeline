WITH MatchData AS
(
    SELECT
        M.MatchID,
        M.MatchDate,
        M.Status,
        M.GameWeek,

        M.HomeTeamID,
        M.HomeTeamName,
        M.AwayTeamID,
        M.AwayTeamName,

        M.HomeGoals,
        M.AwayGoals,
        M.SourceTotalGoals,

        M.HomeXG,
        M.AwayXG,

        M.StadiumName,
        M.StadiumLocation

    FROM Bronze.RawFootballData AS R

    CROSS APPLY OPENJSON(
        R.ResponseJSON,
        '$.data.matches'
    )
    WITH
    (
        MatchID BIGINT '$.match_id',
        MatchDate DATETIME2 '$.match_date',
        Status NVARCHAR(50) '$.status',
        GameWeek INT '$.game_week',

        HomeTeamID BIGINT '$.home_team.team_id',
        HomeTeamName NVARCHAR(150) '$.home_team.team_name',

        AwayTeamID BIGINT '$.away_team.team_id',
        AwayTeamName NVARCHAR(150) '$.away_team.team_name',

        HomeGoals INT '$.score.home',
        AwayGoals INT '$.score.away',
        SourceTotalGoals INT '$.score.total_goals',

        HomeXG DECIMAL(10,3) '$.xg.home',
        AwayXG DECIMAL(10,3) '$.xg.away',

        StadiumName NVARCHAR(200) '$.venue.stadium_name',
        StadiumLocation NVARCHAR(200) '$.venue.stadium_location'
    ) AS M
)

SELECT
    COUNT(*) AS TotalMatches,

    COUNT(DISTINCT MatchID) AS UniqueMatches,

    COUNT(*) - COUNT(DISTINCT MatchID) AS DuplicateMatches,

    MIN(MatchDate) AS EarliestMatch,

    MAX(MatchDate) AS LatestMatch,

    SUM(CASE
        WHEN HomeTeamName IS NULL OR AwayTeamName IS NULL
        THEN 1 ELSE 0
    END) AS MissingTeamNames,

    SUM(CASE
        WHEN HomeGoals IS NULL OR AwayGoals IS NULL
        THEN 1 ELSE 0
    END) AS MissingScores,

    SUM(CASE
        WHEN SourceTotalGoals <> HomeGoals + AwayGoals
        THEN 1 ELSE 0
    END) AS IncorrectTotalGoals,

    SUM(CASE
        WHEN StadiumName IS NULL OR LTRIM(RTRIM(StadiumName)) = ''
        THEN 1 ELSE 0
    END) AS MissingStadiumNames,

    SUM(CASE
        WHEN StadiumLocation IS NULL OR LTRIM(RTRIM(StadiumLocation)) = ''
        THEN 1 ELSE 0
    END) AS MissingStadiumLocations

FROM MatchData;


SELECT
    COUNT(*) AS TotalMatches,

    SUM(CASE
        WHEN StadiumName IS NULL
        THEN 1 ELSE 0
    END) AS NullStadiumNames,

    SUM(CASE
        WHEN LTRIM(RTRIM(StadiumName)) = ''
        THEN 1 ELSE 0
    END) AS EmptyStadiumNames,

    SUM(CASE
        WHEN StadiumLocation IS NULL
        THEN 1 ELSE 0
    END) AS NullStadiumLocations,

    SUM(CASE
        WHEN LTRIM(RTRIM(StadiumLocation)) = ''
        THEN 1 ELSE 0
    END) AS EmptyStadiumLocations

FROM
(
    SELECT
        M.StadiumName,
        M.StadiumLocation

    FROM Bronze.RawFootballData AS R

    CROSS APPLY OPENJSON(
        R.ResponseJSON,
        '$.data.matches'
    )
    WITH
    (
        StadiumName NVARCHAR(200) '$.venue.stadium_name',
        StadiumLocation NVARCHAR(200) '$.venue.stadium_location'
    ) AS M
) AS VenueData;