/*Bronze data confirmation*/

SELECT
    COUNT(*) AS TotalAPIBatches,
    SUM(M.MatchCount) AS TotalMatches
FROM Bronze.RawFootballData AS RFD
CROSS APPLY
(
    SELECT COUNT(*) AS MatchCount
    FROM OPENJSON(
        R.ResponseJSON,
        '$.data.matches'
    )
) AS M;