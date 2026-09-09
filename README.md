# International Population Trends Analysis

## Overview
This project explores demographic change using data from the U.S. Census International Database (IDB). The analysis focuses on a few key indicators to identify trends in population growth, fertility, mortality, and age structure across countries and regions.

The project covers the core topics from Weeks 0-5:

1. Data Literacy
2. Python
3. Relational Databases and SQL
4. Pandas
5. Visualizations

## Project Goal
We want to use real-world demographic data to answer important questions about how populations are changing over time. This project will help us practice extracting, cleaning, transforming, and analyzing data, then storing it in a relational database and presenting findings through clear visualizations.

## Research Focus
The dataset will be used to identify trends such as:

- Countries that skew young, middle-age, or older
- Population increase or decrease by country and region
- Fertility rate patterns by country and region
- Infant mortality trends by country and region
- Births and deaths by country and region
- Life expectancy at birth by country and region
- Net international migration by country and region

For this project, we will keep the scope manageable by focusing on a subset of these indicators rather than trying to analyze every variable available in the dataset.

## Scenario
The International Database helps the U.S. government and the public answer fundamental questions about the people and places of the world. These data are used for planning, policymaking, education, and research.

We will analyze this dataset to identify population trends and better understand how demographic conditions change over time across countries and world regions.

> Source: U.S. Census Bureau. (n.d.). International Database. https://www.census.gov/programs-surveys/international-programs/about/idb.html

## Data Sources
### Primary Dataset
- U.S. Census Bureau. International Database (IDB): World Population Estimates and Projections
  https://www.census.gov/programs-surveys/international-programs/about/idb.html

- Direct dataset download:
  https://www.census.gov/data-tools/demo/data/idb/dataset/idbzip.zip

### Additional Reference Resources
- International Database API:
  https://www.census.gov/data/developers/data-sets/international-database.html

- Geographic identifiers:
  https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html

- Countries and areas:
  https://www.census.gov/programs-surveys/international-programs/about/idb/countries-and-areas.html

## Project Workflow
This project follows a realistic data workflow:

1. Review and understand the dataset
2. Define a focused research question and hypotheses
3. Design a simple SQL schema and ER model
4. Communicate with IDB API and extract relevant data
5. Clean and transform the relevant database fields in Python and Pandas
6. Load the cleaned data into a relational database
7. Create visualizations using the SQL-backed data
8. Write a final report with findings and supporting visuals

## Tools and Technologies
- Python
- Pandas
- SQL
- SQLite or another relational database
- Dash for visualizations
- Git and GitHub for planning and version control

## Expected Deliverables
- Project plan
- ER diagram
- ETL documentation
- SQL schema
- Sketches and outlines
- Dash visualizations and reports
- Final report

## Proposed Scope
To keep the project manageable, the analysis will focus on a smaller set of indicators such as:

- Population growth/age by country & year

## Example Hypotheses
- Countries with lower fertility rates may show older age distributions over time.
- Regions with higher infant mortality may also display lower life expectancy.
- Population growth may be strongest in countries with a relatively younger age structure.

### Current Hypothesis
- USA has an aging population & life expectancy is going up

## Repository Notes
This repository will be used to store:

- Project planning documents
- Data source references
- ETL notes
- SQL scripts and schema files
- Visualization and analysis files
- Final report materials

## Project Documentation
For a full planning breakdown with tasks, timeline, and milestone structure, see [DevelopmentPlan.md](DevelopmentPlan.md).

## Summary
This project demonstrates the full lifecycle of a data project: from finding a real dataset, to shaping a simple database model, to cleaning and loading data, to building dashboard-driven insights. The final result will be a clear, evidence-based report supported by visualizations and SQL-backed analysis.
