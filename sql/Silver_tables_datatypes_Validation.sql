/****Table confirmation***/
SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'Silver'
  AND TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;


/**Inspect the columns and data types**/
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    NUMERIC_PRECISION,
    NUMERIC_SCALE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'Silver'
ORDER BY TABLE_NAME, ORDINAL_POSITION;


/**inspect foreign keys*/
SELECT
    fk.name AS ForeignKeyName,
    OBJECT_SCHEMA_NAME(fk.parent_object_id) AS SchemaName,
    OBJECT_NAME(fk.parent_object_id) AS TableName,
    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS ColumnName,
    OBJECT_SCHEMA_NAME(fk.referenced_object_id) AS ReferencedSchema,
    OBJECT_NAME(fk.referenced_object_id) AS ReferencedTable,
    COL_NAME(fkc.referenced_object_id, fkc.referenced_column_id) AS ReferencedColumn
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc
    ON fk.object_id = fkc.constraint_object_id
WHERE OBJECT_SCHEMA_NAME(fk.parent_object_id) = 'Silver'
ORDER BY TableName, ForeignKeyName;


/**Inspect primary keys**/
SELECT
    tc.TABLE_NAME,
    tc.CONSTRAINT_NAME,
    kcu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
INNER JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu
    ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
    AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
WHERE tc.TABLE_SCHEMA = 'Silver'
  AND tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
ORDER BY tc.TABLE_NAME;