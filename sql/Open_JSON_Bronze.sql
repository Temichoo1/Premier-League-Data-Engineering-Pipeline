SELECT
    [key] AS MatchArrayPosition,
    value AS MatchJSON
FROM Bronze.RawFootballData
CROSS APPLY OPENJSON(ResponseJSON, '$.data.matches');