/*Duplicate checks*/

SELECT
    MatchID,
    COUNT(*) AS RecordCount
FROM Gold.MatchAnalysis
GROUP BY MatchID
HAVING COUNT(*) > 1;

/*total matches checks*/

SELECT
    MatchResult,
    COUNT(*) AS MatchCount
  
FROM Gold.MatchAnalysis
GROUP BY MatchResult
ORDER BY MatchResult;

/*winning team logic*/
SELECT *
FROM Gold.MatchAnalysis
WHERE
    (MatchResult = 'H' AND HomeGoals <= AwayGoals)
    OR
    (MatchResult = 'A' AND AwayGoals <= HomeGoals)
    OR
    (MatchResult = 'D' AND HomeGoals <> AwayGoals);