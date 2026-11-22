/**Remaining data investigation */


/*Confirm the pagination information stored in our Bronze layer*/
SELECT
    JSON_VALUE(ResponseJSON, '$.data.total') AS TotalMatches,
    JSON_VALUE(ResponseJSON, '$.data.current_page') AS CurrentPage,
    JSON_VALUE(ResponseJSON, '$.data.last_page') AS TotalPages,
    JSON_VALUE(ResponseJSON, '$.data.per_page') AS PageSize
FROM Bronze.RawFootballData;

/*The NULL values suggest that our JSON paths don't match the actual structure of the API response*/


SELECT
    [key] AS JSONProperty,
    value AS PropertyValue,
    type AS JSONDataType
FROM Bronze.RawFootballData
CROSS APPLY OPENJSON(ResponseJSON);

SELECT
    [key] AS JSONProperty,
    value AS PropertyValue,
    type AS JSONDataType
FROM Bronze.RawFootballData
CROSS APPLY OPENJSON(ResponseJSON, '$.data');

SELECT
    COUNT(*) AS NumberOfMatches
FROM Bronze.RawFootballData AS R
CROSS APPLY OPENJSON(
    R.ResponseJSON,
    '$.data.matches'
);