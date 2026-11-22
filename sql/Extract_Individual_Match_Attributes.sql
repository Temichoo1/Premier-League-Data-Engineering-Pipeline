/*Extract individual match attributes*/

SELECT
    M.match_id,
    M.match_date,
    M.status,
    M.game_week,
    M.home_team,
    M.away_team,
    M.home_goals,
    M.away_goals
FROM Bronze.RawFootballData AS RFD
CROSS APPLY OPENJSON(RFD.ResponseJSON, '$.data.matches')
WITH
(
    match_id INT '$.match_id',
    match_date DATETIME2 '$.match_date',
    status NVARCHAR(50) '$.status',
    game_week INT '$.game_week',
    home_team NVARCHAR(100) '$.home_team.team_name',
    away_team NVARCHAR(100) '$.away_team.team_name',
    home_goals INT '$.score.home',
    away_goals INT '$.score.away'
) AS M;