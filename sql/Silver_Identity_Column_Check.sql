SELECT
    COLUMN_NAME,
    COLUMNPROPERTY(
        OBJECT_ID('Silver.Venues'),
        COLUMN_NAME,
        'IsIdentity'
    ) AS IsIdentity
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_NAME = 'Venues';

  DBCC CHECKIDENT ('Silver.Venues', NORESEED);