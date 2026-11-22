SELECT 'Leagues' AS TableName, COUNT(*) AS RecordCount FROM Silver.Leagues
UNION ALL
SELECT 'Seasons', COUNT(*) FROM Silver.Seasons
UNION ALL
SELECT 'Teams', COUNT(*) FROM Silver.Teams
UNION ALL
SELECT 'Venues', COUNT(*) FROM Silver.Venues
UNION ALL
SELECT 'Matches', COUNT(*) FROM Silver.Matches
UNION ALL
SELECT 'MatchScores', COUNT(*) FROM Silver.MatchScores
UNION ALL
SELECT 'MatchStatistics', COUNT(*) FROM Silver.MatchStatistics;