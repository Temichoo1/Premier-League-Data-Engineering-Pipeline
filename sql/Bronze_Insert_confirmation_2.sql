SELECT
    RawDataID,
    SourceSystem,
    Endpoint,
    ExtractedAt,
    DATALENGTH(ResponseJSON) AS JSONSizeBytes
FROM Bronze.RawFootballData
ORDER BY RawDataID;

SELECT
    RawDataID,
    COUNT(*) AS MatchCount
FROM Bronze.RawFootballData AS R
CROSS APPLY OPENJSON(
    R.ResponseJSON,
    '$.data.matches'
)
GROUP BY RawDataID
ORDER BY RawDataID;

