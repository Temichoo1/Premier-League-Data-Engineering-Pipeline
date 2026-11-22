CREATE TABLE Gold.MatchAnalysis
(
    MatchID INT NOT NULL PRIMARY KEY,
    MatchDate DATETIME2 NOT NULL,
    SeasonYear INT NOT NULL,
    GameWeek INT NULL,

    HomeTeam NVARCHAR(150) NOT NULL,
    AwayTeam NVARCHAR(150) NOT NULL,

    HomeGoals INT NOT NULL,
    AwayGoals INT NOT NULL,
    TotalGoals INT NOT NULL,

    MatchResult CHAR(1) NOT NULL,
    WinningTeam NVARCHAR(150) NULL,

    StadiumName NVARCHAR(200) NULL,
    StadiumLocation NVARCHAR(250) NULL,

    HomeXG DECIMAL(6,3) NULL,
    AwayXG DECIMAL(6,3) NULL,
    TotalXG DECIMAL(6,3) NULL,

    HomeWinOdds DECIMAL(10,4) NULL,
    DrawOdds DECIMAL(10,4) NULL,
    AwayWinOdds DECIMAL(10,4) NULL,

    HomeWinProbability DECIMAL(7,4) NULL,
    DrawProbability DECIMAL(7,4) NULL,
    AwayWinProbability DECIMAL(7,4) NULL,

    LoadedAt DATETIME2 NOT NULL
        DEFAULT SYSDATETIME()
);