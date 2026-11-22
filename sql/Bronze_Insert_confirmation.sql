select * from Bronze.RawFootballData

SELECT
    RawDataID,
    SourceSystem,
    Endpoint,
    ExtractedAt,
    ISJSON(ResponseJSON) AS IsValidJSON,
    LEN(ResponseJSON) AS JSONLength
FROM Bronze.RawFootballData;
