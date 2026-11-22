CREATE TABLE Bronze.RawFootballData
(
    RawDataID BIGINT IDENTITY(1,1) PRIMARY KEY,

    SourceSystem NVARCHAR(100) NOT NULL,

    Endpoint NVARCHAR(500) NOT NULL,

    ResponseJSON NVARCHAR(MAX) NOT NULL,

    ExtractedAt DATETIME2 NOT NULL,

    SourceSystem NVARCHAR(100) NULL
    
    DEFAULT SYSUTCDATETIME(), --This means SQL Server automatically records the UTC extraction timestamp if Python doesn't supply one
    
    

    CONSTRAINT CK_RawFootballData_ValidJSON
        CHECK (ISJSON(ResponseJSON) = 1) --This tells SQL Server to check whether the supplied response is valid JSON before accepting it.
);


/* Confirm the table exists**/
SELECT *
FROM Bronze.RawFootballData;