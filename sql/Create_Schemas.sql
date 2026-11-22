/***  CREATE SCHEMAS   ***/

USE PremierLeagueDW; 	
GO

CREATE SCHEMA Bronze; --Raw data extracted from our API.
GO

CREATE SCHEMA Silver; --Cleaned and transformed data.
GO

CREATE SCHEMA Gold;  --Analytics-ready data for reporting.
GO