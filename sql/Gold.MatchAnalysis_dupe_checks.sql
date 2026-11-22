SELECT
    MatchID,
    COUNT(*) AS RecordCount
FROM Gold.MatchAnalysis
GROUP BY MatchID
HAVING COUNT(*) > 1;