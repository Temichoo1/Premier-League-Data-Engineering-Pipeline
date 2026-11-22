/**CREATE SILVER TABLES**/

CREATE TABLE Silver.Leagues
(
    LeagueID INT NOT NULL,
    LeagueName NVARCHAR(150) NOT NULL,
    Country NVARCHAR(100) NULL,
    CompetitionName NVARCHAR(150) NULL,
    LeagueImage NVARCHAR(500) NULL,

    CONSTRAINT PK_Silver_Leagues
        PRIMARY KEY (LeagueID)
);

SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'Leagues';

CREATE TABLE Silver.Teams
(
    TeamID INT NOT NULL,
    TeamName NVARCHAR(150) NOT NULL,
    TeamLogo NVARCHAR(500) NULL,

    CONSTRAINT PK_Silver_Teams
        PRIMARY KEY (TeamID)
);

SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'Teams';

CREATE TABLE Silver.Venues
(
    VenueID INT IDENTITY(1,1) NOT NULL,
    StadiumName NVARCHAR(200) NOT NULL,
    StadiumLocation NVARCHAR(250) NULL,

    CONSTRAINT PK_Silver_Venues
        PRIMARY KEY (VenueID),

    CONSTRAINT UQ_Silver_Venues_StadiumName
        UNIQUE (StadiumName)
);
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'Venues';

CREATE TABLE Silver.Seasons
(
    SeasonID INT NOT NULL,
    LeagueID INT NOT NULL,
    SeasonYear INT NOT NULL,

    CONSTRAINT PK_Silver_Seasons
        PRIMARY KEY (SeasonID),

    CONSTRAINT FK_Silver_Seasons_Leagues
        FOREIGN KEY (LeagueID)
        REFERENCES Silver.Leagues (LeagueID)
);
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'Seasons';

CREATE TABLE Silver.Matches
(
    MatchID INT NOT NULL,
    SeasonID INT NOT NULL,
    MatchDate DATETIME2 NOT NULL,
    DateUnix BIGINT NULL,
    MatchStatus NVARCHAR(50) NULL,
    MatchStatusLocalized NVARCHAR(100) NULL,
    RoundID INT NULL,
    GameWeek INT NULL,
    HomeTeamID INT NOT NULL,
    AwayTeamID INT NOT NULL,
    VenueID INT NULL,
    WinnerText NVARCHAR(150) NULL,
    LastUpdated DATETIME2 NULL,

    CONSTRAINT PK_Silver_Matches
        PRIMARY KEY (MatchID),

    CONSTRAINT FK_Silver_Matches_Seasons
        FOREIGN KEY (SeasonID)
        REFERENCES Silver.Seasons (SeasonID),

    CONSTRAINT FK_Silver_Matches_HomeTeam
        FOREIGN KEY (HomeTeamID)
        REFERENCES Silver.Teams (TeamID),

    CONSTRAINT FK_Silver_Matches_AwayTeam
        FOREIGN KEY (AwayTeamID)
        REFERENCES Silver.Teams (TeamID),

    CONSTRAINT FK_Silver_Matches_Venues
        FOREIGN KEY (VenueID)
        REFERENCES Silver.Venues (VenueID)
);
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'Matches';

CREATE TABLE Silver.MatchScores
(
    MatchID INT NOT NULL,
    HomeGoals INT NOT NULL,
    AwayGoals INT NOT NULL,
    SourceTotalGoals INT NULL,
    CalculatedTotalGoals INT NOT NULL,
    IsScoreValid BIT NOT NULL,

    CONSTRAINT PK_Silver_MatchScores
        PRIMARY KEY (MatchID),

    CONSTRAINT FK_Silver_MatchScores_Matches
        FOREIGN KEY (MatchID)
        REFERENCES Silver.Matches (MatchID),

    CONSTRAINT CK_Silver_MatchScores_HomeGoals
        CHECK (HomeGoals >= 0),

    CONSTRAINT CK_Silver_MatchScores_AwayGoals
        CHECK (AwayGoals >= 0),

    CONSTRAINT CK_Silver_MatchScores_CalculatedTotal
        CHECK (CalculatedTotalGoals = HomeGoals + AwayGoals)
);
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'MatchScores';


CREATE TABLE Silver.MatchStatistics
(
    MatchID INT NOT NULL,

    HomeXG DECIMAL(6,3) NULL,
    AwayXG DECIMAL(6,3) NULL,
    TotalXG DECIMAL(6,3) NULL,

    HomeWinOdds DECIMAL(10,4) NULL,
    DrawOdds DECIMAL(10,4) NULL,
    AwayWinOdds DECIMAL(10,4) NULL,

    HomeWinProbability DECIMAL(7,4) NULL,
    DrawProbability DECIMAL(7,4) NULL,
    AwayWinProbability DECIMAL(7,4) NULL,

    CONSTRAINT PK_Silver_MatchStatistics
        PRIMARY KEY (MatchID),

    CONSTRAINT FK_Silver_MatchStatistics_Matches
        FOREIGN KEY (MatchID)
        REFERENCES Silver.Matches (MatchID)
);
SELECT *
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'MatchStatistics';


