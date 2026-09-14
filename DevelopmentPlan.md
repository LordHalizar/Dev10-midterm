# Development Plan

## Project Title
International Population Trends Analysis

## Course Context
This project applies the concepts from Weeks 0-5:

- Data Literacy
- Python
- Relational Databases and SQL
- Pandas
- Visualizations

The goal is to analyze a real-world population dataset, clean and transform it, load it into a SQL database, and create visualizations that support research questions about population change over time.

## Scenario
The International Database (IDB) contains demographic population estimates and projections for countries and regions. We will use the dataset to explore demographic trends and identify patterns in population composition and change over time.

The project will focus on a few key questions, such as:

- Which countries are trending younger, middle-aged, or older?
- Which countries and regions are experiencing population growth or decline?
- How do fertility rates vary across countries and regions?
- How do infant mortality and life expectancy compare over time?
- Which countries are seeing the strongest birth and death trends?

This project will keep the scope manageable by focusing on a small set of agreed-upon measures rather than attempting to analyze every available variable.

## Research Questions and Hypotheses

### Primary Questions
1. Which countries have the youngest and oldest age structures?
2. Which countries and regions show the strongest population growth or decline?
3. How do fertility and life expectancy trends differ between countries and world regions?
4. Which demographic indicators are most strongly associated with population change over time?

### Sample Hypotheses
- Countries with lower fertility rates may also have older median age profiles.
- High-income countries may show slower population growth or decline, while lower-income countries may show faster growth.
- Regions with lower infant mortality and higher life expectancy may show different population trajectories than regions with higher mortality rates.

### Current Hypothesis
- USA has an aging population and Americans will be having fewer children

## Data Sources
The main data source for this project is the U.S. Census International Database (IDB), including population estimates and projections.

### Primary Data Source
- U.S. Census Bureau. (n.d.). International Database (IDB): World population estimates and projections. https://www.census.gov/programs-surveys/international-programs/about/idb.html
- U.S. Census Bureau. (n.d.). International Database dashboard. https://www.census.gov/data-tools/demo/idb/#/dashboard
- U.S. Census Bureau. (n.d.). International Database ZIP file. https://www.census.gov/data-tools/demo/data/idb/dataset/idbzip.zip

### Supporting Resources
- U.S. Census Bureau. (n.d.). International Database API documentation. https://www.census.gov/data/developers/data-sets/international-database.html
- U.S. Census Bureau. (n.d.). Geographic identifiers guidance. https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html
- U.S. Census Bureau. (n.d.). Countries and areas. https://www.census.gov/programs-surveys/international-programs/about/idb/countries-and-areas.html

The team will use only a subset of the available data to keep the project simple, focused, and realistic.

## Scope and Simplification Strategy
The project will follow the KISS principle and keep the main analysis narrow and manageable.

### Planned Focus
- Country-level population data
- Total population ranges
- Predictive population rates (life expectancy, mortality, natural growth rate, etc.)
- population data based on collection year

### Excluded or Delayed Topics
- Full multi-table schema for every possible IDB measure
- Every nation-level demographic variable in the dataset
- Complex geospatial mapping unless time allows

The project will first complete a working version for country and population trends, then add one or two additional indicators such as fertility or mortality if needed.

## Project Management Approach
We will break the work into small tasks that can be completed in 0.5 to 4 hours each, with actual time recorded after each task is completed.

### Recommended Tool
GitHub Projects is recommended for tracking tasks, but a spreadsheet or markdown checklist is acceptable if needed.

## Data Model Concept
The dataset can be modeled in a simplified structure designed for analysis and SQL loading.

### Entity Types
- Country
- Year
- Population Range Indicators
- Population Records
- Population Age Indicator

### Database Design Breakdown
Database Tables:

- [x] Country
    - country id (primary key)
    - country code
    - country name
- [x] Population Rate
    - population rate id (primary key)
    - population age-range (0-4)
    - population age-range (5-9)
    - population age-range (10-14)
    - population age-range (15-19)
    - population age-range (20-24)
    - population age-range (25-29)
    - population age-range (30-34)
    - population age-range (35-39)
    - population age-range (40-44)
    - population age-range (45-49)
    - population age-range (50-54)
    - population age-range (55-59)
    - population age-range (60-64)
    - population age-range (65-69)
    - population age-range (70-74)
    - population age-range (75-79)
    - population age-range (80-84)
    - population age-range (85-89)
    - population age-range (90-94)
    - population age-range (95-99)
    - population age-range (100+)
- [x] Population Data
    - population data id (primary key)
    - year
    - median age
    - country id (foreign key)
    - population range id (foreign key)

This keeps the model simple while still supporting analysis across time and geography.

## ETL Development Breakdown

### Phase 1: Project Setup and Planning
- [x] Review assignment requirements and scope (Estimated: 1 hour) — Confirm deliverables.
- [x] Create GitHub repository and branch (Estimated: 1 hour) — Private repo; add instructor as collaborator.
- [x] Add .gitignore and project structure (Estimated: 0.5 hour) — Keep repo clean.
- [x] Create project plan and task tracker (Estimated: 2 hour) — Use GitHub Projects or a markdown checklist.
- [x] Instructor review / approval (Estimated: 0.5-1 hour) — Optional, but recommended.

### Phase 2: Data Collection and Evaluation
- [x] Download IDB data (Estimated: 0.5 hour) — Use the ZIP or API access.
- [x] Review data dictionary and columns (Estimated: 1-2 hours) — Identify relevant variables.
- [x] Inspect file format and structure (Estimated: 1 hour) — Check CSV, TXT, or other source files.
- [x] Confirm key fields and country identifiers (Estimated: 1 hour) — Use GEOID and country metadata.

### Phase 3: Data Modeling and SQL Design
- [x] Perform exploratory data analysis (Estimated: 2-3 hours) — Review distributions and missing values.
- [x] Design conceptual schema (Estimated: 2 hours) — Country, year, indicator, value.
- [x] Create ER diagram (Estimated: 2 hours) — Simple 2NF-friendly model.
- [x] Draft SQL schema and DDL (Estimated: 2 hours) — Create tables and constraints.

### Phase 4: ETL Preparation
- [x] Install/Download requirements
    - os
    - pandas
    - dynaconf
    - sqlalchemy
    - International Database dataset
- [x] Extraction steps (0.5 hour).
    - define directory path for locating IDB dataset.
    - extract using "read_csv" pandas method.
    - define delimiter as "|"
- [x] Define transformation steps (4-6 hours).
    - custom transformations for each table.
    - rename columns to match database.
    - filter to only required columns.
    - clean data to match database variable formats.
- [x] Define load steps (Estimated: 1-2 hours).
    - load transformed data into PostgreSQL database.
    - load to database using "to_sql" pandas method
    - custom loading for table with foreign key values
- [x] Document ETL process (Estimated: 1-2 hours) — Include in the final report.

### Phase 5: Visualizations and Reporting
- [x] Install/Download requirements
    - dash
    - plotly
- [x] Design dashboard layouts (Estimated: 1-2 hours) — Decide on charts and filters.
- [x] Build Dash visualizations (Estimated: 8-10 hours) — At least one per dataset or indicator.
- [x] Create report with findings (Estimated: 2-3 hours) — Include narrative and citations.
- [x] Gather peer feedback (Estimated: 1 hour) — Integrate revisions.

## ETL Workflow

### Extraction
1. Download the IDB ZIP data file or use the API to retrieve the relevant dataset.
2. Review the metadata and variable descriptions.
3. Identify which files and records are relevant to the project scope.
4. Load the raw files into a working notebook or local data directory.

### Transformation
1. Read the raw data into Python using Pandas.
2. Review column names, data types, and missing values.
3. Filter to the country/region and year ranges relevant to the research question.
4. Rename columns to clear and consistent names.
5. Convert values to appropriate numeric types.
6. Standardize country and region identifiers.
7. Create a clean table ready for SQL insertion.

### Load
1. Create the SQL schema using DDL.
2. Validate the transformed data against the schema.
3. Insert cleaned records into the database.
4. Test queries for data integrity and correctness.
5. Use the SQL tables as the source for visualizations.

## Visualization Plan
The final dashboard contains:

- A title slide or introduction tile
- At least one chart per dataset or indicator used
- Clear labels for axes, titles, and values
- Filters and sorting options for reports
- Data driven directly from the SQL tables

### Visualizations
- [x] Line chart: population over time for selected countries
- [x] Bar chart: median age over time for all countries
- [x] Horizontal bar chart: age-ranges over time for selected country

## Report Plan
The final report will include:

- A description of the dataset and its source
- Research question and hypothesis
- Explanation of the data cleaning and transformation steps
- Visualizations that support findings
- A brief summary of trends discovered
- Correlation analysis when relevant
- Peer feedback and revisions

## Deliverables Checklist
The final submission should include:

- [x] Project plan
- [x] ER diagram
- [x] ETL documentation
- [x] SQL schema
- [x] Sketches/outlines
- [x] Dash visualizations
- [x] Final report

## Success Criteria
The project is successful if it:

- Uses a real dataset from the IDB or related census sources
- Applies concepts from Python, SQL, Pandas, and visualizations
- Demonstrates a clear ETL workflow
- Produces at least one meaningful analytical narrative
- Connects the data to a research question or hypothesis
- Shows evidence of iterative planning and improvement

## Final Notes
This project should remain intentionally practical and focused. The best project is not the most complex one; it is the one that clearly demonstrates good data analysis, careful transformation, sound SQL structure, and interpretable visualizations.
