# ⚽ Premier League Data Engineering Pipeline

## Overview

This project is an end-to-end data engineering pipeline built using Python and Microsoft SQL Server. It ingests Premier League football data from the Football-Data.io API, stores the raw API responses in a Bronze layer, and transforms the data into structured relational datasets within a Silver layer.

The project follows the Medallion Architecture (Bronze, Silver, Gold), providing a scalable foundation for data ingestion, transformation, data quality validation, and analytical modelling.

The pipeline is designed to demonstrate practical data engineering skills, including API ingestion, JSON processing, ETL orchestration, relational database design, data quality checks, and transactional data loading.

---

## Architecture

The pipeline follows the Medallion Architecture.

```text
Football-Data.io API
        │
        ▼
┌───────────────────────────┐
│       BRONZE LAYER       │
│                           │
│ Raw JSON API responses   │
│ SQL Server storage       │
│ Source data preservation │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│       SILVER LAYER       │
│                           │
│ JSON flattening          │
│ Data cleaning            │
│ Deduplication            │
│ Data validation          │
│ Relational modelling      │
└──────────────┬────────────┘
               │
               ▼
┌───────────────────────────┐
│        GOLD LAYER        │
│                           │
│ Analytical datasets      │
│ Reporting models         │
│ Business-ready data     │
│        Planned           │
└───────────────────────────┘
```

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL development and data transformation |
| Microsoft SQL Server | Data storage and relational modelling |
| SQL Server Management Studio (SSMS) | Database management, querying and validation |
| Visual Studio Code | Python development environment |
| SQLAlchemy | Database connectivity and integration |
| pyodbc | SQL Server connectivity |
| Pandas | Data manipulation and processing |
| Requests | API communication |
| Python-dotenv | Environment variable management |
| Git & GitHub | Version control and project documentation |

---

## Data Source

**Football-Data.io API**

The pipeline retrieves Premier League match data from the Football-Data.io API.

| Attribute | Value |
|---|---|
| Source | Football-Data.io |
| Competition | English Premier League |
| League ID | 15 |
| Season | 2025/2026 |
| Season ID | 189 |
| Matches extracted | 381 |
| API endpoint | `/api/v1/seasons/189/matches` |

The API returns JSON responses containing match information, including teams, scores, match dates, league details, season information, stadium details, expected goals, betting odds, and win probabilities.

API responses are paginated, with the pipeline retrieving multiple pages of results to collect the full dataset.

---

# Data Pipeline

## 🥉 Bronze Layer – Raw Data Ingestion

The Bronze layer is responsible for extracting data from the Football-Data.io API and preserving the original source responses.

### Implemented functionality

- API data ingestion using Python.
- API pagination.
- HTTP request handling.
- Retrieval of match data across multiple pages.
- Raw JSON storage in Microsoft SQL Server.
- Source endpoint tracking.
- Extraction timestamp tracking.
- Preservation of original source data for downstream processing and re-extraction.

### Bronze database table

`Bronze.RawFootballData`

| Column | Description |
|---|---|
| RawDataID | Unique identifier for each raw data record |
| SourceSystem | Source of the extracted data |
| Endpoint | API endpoint used for extraction |
| ResponseJSON | Raw API response stored as JSON |
| ExtractedAt | Timestamp when the data was extracted |

### Extraction results

| Page | Records |
|---|---:|
| Page 1 | 100 |
| Page 2 | 100 |
| Page 3 | 100 |
| Page 4 | 81 |
| **Total matches** | **381** |

Four raw API responses were successfully stored in the Bronze layer.

---

## 🥈 Silver Layer – Data Transformation & Modelling

The Silver layer extracts the raw JSON responses from Bronze, flattens nested JSON structures, cleans the data, and separates it into relational datasets.

### Implemented functionality

- Extraction of raw JSON data from SQL Server.
- JSON parsing using Python.
- Flattening of nested JSON structures.
- Data cleaning and standardisation.
- Deduplication of teams and venues.
- Generation of unique team and venue identifiers.
- Handling of missing stadium information.
- Transformation into structured relational datasets.
- Data quality validation.
- Identification of inconsistencies in source data.

### Silver transformation process

```text
Bronze.RawFootballData
        │
        ▼
Extract Bronze Records
        │
        ▼
Parse JSON Responses
        │
        ▼
Flatten Nested Match Objects
        │
        ▼
Clean & Standardise Data
        │
        ▼
Build Relational Datasets
        │
        ▼
Validate Data Quality
        │
        ▼
Load Silver Tables
```

### Silver database tables

The Silver layer consists of seven relational tables.

| Table | Description |
|---|---|
| Silver.Leagues | Competition and league information |
| Silver.Seasons | Season information associated with leagues |
| Silver.Teams | Unique teams participating in the competition |
| Silver.Venues | Unique stadiums and their locations |
| Silver.Matches | Match details, dates, teams, and venue relationships |
| Silver.MatchScores | Match scores and total goal calculations |
| Silver.MatchStatistics | Expected goals, odds, and win probabilities |

### Relational modelling

The Silver layer uses primary keys and foreign keys to establish relationships between entities and maintain referential integrity.

The model separates match details, scoring information, and statistical information into dedicated tables.

Key relationships include:

- Seasons → Leagues
- Matches → Seasons
- Matches → Home Teams
- Matches → Away Teams
- Matches → Venues
- MatchScores → Matches
- MatchStatistics → Matches

The `VenueID` in the Matches table is nullable to accommodate matches where stadium information is unavailable in the source API.

---

## Data Quality & Validation

Data quality checks were implemented to assess the extracted dataset before loading it into the Silver layer.

### Initial source data quality results

| Validation | Result |
|---|---:|
| Total matches | 381 |
| Unique matches | 381 |
| Duplicate matches | 0 |
| Missing team names | 0 |
| Missing scores | 0 |
| Incorrect source total goals | 6 |
| Matches with missing stadium names | 117 |
| Matches with missing stadium locations | 117 |

### Data quality handling

- Duplicate matches were checked using match identifiers.
- Team names were checked for missing values.
- Scores were checked for missing values.
- Source total goals were compared against calculated home and away goals.
- Missing stadium information was identified and handled.
- Venue records were deduplicated.
- Foreign key relationships were validated.
- Match records were checked for valid team and venue references.

### Source data inconsistencies

Six matches contained inconsistencies between the source API's reported total goals and the calculated total from home and away scores.

Rather than silently correcting the source data, the pipeline retains the source total and calculates the expected total separately.

The `Silver.MatchScores` table includes:

| Column | Description |
|---|---|
| HomeGoals | Goals scored by the home team |
| AwayGoals | Goals scored by the away team |
| SourceTotalGoals | Total goals reported by the API |
| CalculatedTotalGoals | Total calculated using home and away scores |
| IsScoreValid | Flag identifying whether the source total matches the calculated total |

This allows source data quality issues to be identified and investigated without losing the original information.

---

## Silver Layer Load Process

The Silver layer is loaded using a Python-based SQL Server loader.

### Loading features

- Dynamic SQL INSERT statement generation.
- Parameterised SQL queries.
- Bulk inserts using `cursor.executemany()`.
- Foreign key-aware table loading order.
- Full refresh strategy.
- Transaction management.
- Rollback on failure.
- Identity column handling.

### Full refresh strategy

The Silver layer currently uses a full refresh approach.

Before loading new data, the existing Silver tables are cleared in dependency order to prevent foreign key violations.

The tables are then populated in the correct order:

1. Leagues
2. Seasons
3. Teams
4. Venues
5. Matches
6. MatchScores
7. MatchStatistics

The entire refresh is wrapped in a SQL transaction.

If an error occurs during the refresh, the transaction is rolled back to prevent an incomplete dataset from being left in the Silver layer.

---

## Current Silver Layer Results

The following records have successfully been prepared and loaded into Microsoft SQL Server.

| Table | Records Loaded |
|---|---:|
| Leagues | 1 |
| Seasons | 1 |
| Teams | 20 |
| Venues | 14 |
| Matches | 381 |
| MatchScores | 381 |
| MatchStatistics | 381 |
| **Total** | **1,146** |

The Silver layer has been successfully loaded and is ready for post-load validation and downstream analytical modelling.

---

# Project Structure

```text
Premier League Data Engineering Pipeline/
│
├── src/
│   │
│   ├── bronze/
│   │   └── extract_bronze.py
│   │
│   ├── silver/
│   │   ├── extract_bronze.py
│   │   ├── transform_matches.py
│   │   ├── transform_silver.py
│   │   ├── validate_silver.py
│   │   └── load_silver.py
│   │
│   ├── gold/
│   │   └── (planned)
│   │
│   ├── tests/
│   │   └── (planned)
│   │
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*The project structure will evolve as additional pipeline components are developed.*

---

# Security & Configuration

Database connection details and API credentials are managed through environment variables using a `.env` file.

Sensitive credentials are excluded from version control.

Example configuration:

```env
API_KEY=your_api_key
SQL_CONNECTION_STRING=your_connection_string
```

A `.gitignore` file is used to prevent sensitive configuration files, virtual environments, and unnecessary local files from being committed.

---

# Project Status

| Component | Status |
|---|---|
| API integration | ✅ Complete |
| API pagination | ✅ Complete |
| Bronze ingestion | ✅ Complete |
| Raw JSON storage | ✅ Complete |
| Silver extraction | ✅ Complete |
| JSON flattening | ✅ Complete |
| Data cleaning | ✅ Complete |
| Relational modelling | ✅ Complete |
| Data quality validation | ✅ Complete |
| Silver loading | ✅ Complete |
| Transaction management | ✅ Complete |
| Silver post-load validation | 🔄 In progress |
| Gold analytical layer | ⏳ Planned |
| End-to-end orchestration | ⏳ Planned |
| Automated pipeline scheduling | ⏳ Planned |

---

# Future Development

The next stages of development will focus on expanding the pipeline into a fully developed data engineering solution.

### Gold Layer

Develop analytical datasets designed for reporting, analysis, and downstream consumption.

Potential datasets include:

- Team performance analysis.
- League standings.
- Home vs away performance.
- Goals scored and conceded.
- Expected goals analysis.
- Match outcome analysis.
- Season-level performance metrics.

### Further Improvements

- Automated pipeline orchestration.
- Logging and monitoring.
- Automated testing.
- Incremental loading strategies.
- Improved exception handling.
- Data lineage.
- Pipeline scheduling.
- Performance optimisation.
- Analytical reporting and visualisation.

---

# Skills Demonstrated

This project demonstrates practical experience in:

- Python ETL development.
- API data ingestion.
- REST API interaction.
- Pagination.
- JSON processing.
- Data transformation.
- Data cleaning.
- Data deduplication.
- Data quality validation.
- SQL Server database integration.
- Relational database design.
- Primary and foreign key relationships.
- Data modelling.
- Parameterised SQL.
- Bulk data loading.
- Transaction management.
- Error handling.
- Medallion Architecture.
- Data engineering problem-solving.

---

## Project Objective

The objective of this project is to develop a practical understanding of modern data engineering principles by building an end-to-end pipeline using real-world data.

The pipeline provides a foundation for exploring data ingestion, transformation, storage, quality assurance, relational modelling, and analytical processing while progressively incorporating more advanced data engineering technologies and practices.
