import os

import pandas as pd
from callbacks import register_callbacks
from dash import Dash, dcc, html
from dynaconf import Dynaconf
from etl import (
    CountryETLProcessor,
    PopulationDataETLProcessor,
    PopulationRangeETLProcessor,
)
from sqlalchemy import Engine, create_engine

os.chdir(os.path.dirname(__file__))

API_URL = "https://api.census.gov/data/timeseries/idb/5year"

# function to instantiate sqlalchemy-based database connection
def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
    return create_engine(settings.ENGINE_URL, echo=True)

# conglomerate etl function that runs etl for all database tables
def etl_processing(file_path: str, engine: Engine, countries: list[str]):

    country_etl = CountryETLProcessor(
        file_path=file_path, engine=engine, countries=countries
    )
    country_etl.process()

    population_range_etl = PopulationRangeETLProcessor(
        file_path=file_path, engine=engine, countries=countries
    )
    population_range_etl.process()

    population_data_etl = PopulationDataETLProcessor(
        file_path=file_path, engine=engine, countries=countries
    )
    population_data_etl.process()


engine = build_engine()

# country codes used for extraction, transforming, loading, and processing in etl class methods
country_codes = ['W140000WOUS', 'W140000WOFR', 'W140000WOJP', 'W140000WOCN', 'W140000WODE', 'W140000WOIN', 'W140000WOCA', 'W140000WOMX', 'W140000WOKR', 'W140000WOIT']

etl_processing(file_path="idbzip\\idb5yr.txt", engine=engine, countries=country_codes)

app = Dash(__name__, suppress_callback_exceptions=True)

query = "select c.country_name, pd.year, pd.population_total, median_age from population_data pd join country c on c.country_id = pd.country_id"
countries_df = pd.read_sql(query, engine)

query = "select c.country_name, pd.year, pr.pop_range_0_4, pr.pop_range_5_9, pr.pop_range_10_14, pr.pop_range_15_19, pr.pop_range_20_24, pr.pop_range_25_29, pr.pop_range_30_34, pr.pop_range_35_39, pr.pop_range_40_44, pr.pop_range_45_49, pr.pop_range_50_54, pr.pop_range_55_59, pr.pop_range_60_64, pr.pop_range_65_69, pr.pop_range_70_74, pr.pop_range_75_79, pr.pop_range_80_84, pr.pop_range_85_89, pr.pop_range_90_94, pr.pop_range_95_99, pr.pop_range_100 from population_range pr join population_data pd on pd.pop_range_id = pr.pop_range_id join country c on c.country_id = pd.country_id where c.country_name = 'United States'"
us_range_df = pd.read_sql(query, engine)

query = "select pd.year, pd.population_total, pd.median_age, pr.pop_range_0_4, pr.pop_range_5_9, pr.pop_range_10_14, pr.pop_range_15_19, pr.pop_range_20_24, pr.pop_range_25_29, pr.pop_range_30_34, pr.pop_range_35_39, pr.pop_range_40_44, pr.pop_range_45_49, pr.pop_range_50_54, pr.pop_range_55_59, pr.pop_range_60_64, pr.pop_range_65_69, pr.pop_range_70_74, pr.pop_range_75_79, pr.pop_range_80_84, pr.pop_range_85_89, pr.pop_range_90_94, pr.pop_range_95_99, pr.pop_range_100 from population_range pr join population_data pd on pd.pop_range_id = pr.pop_range_id join country c on c.country_id = pd.country_id"
numeric_df = pd.read_sql(query, engine)

# primary query for data frame used in dash visualizations
query = "select c.country_name, pd.year, pd.population_total, pd.median_age, pr.pop_range_0_4, pr.pop_range_5_9, pr.pop_range_10_14, pr.pop_range_15_19, pr.pop_range_20_24, pr.pop_range_25_29, pr.pop_range_30_34, pr.pop_range_35_39, pr.pop_range_40_44, pr.pop_range_45_49, pr.pop_range_50_54, pr.pop_range_55_59, pr.pop_range_60_64, pr.pop_range_65_69, pr.pop_range_70_74, pr.pop_range_75_79, pr.pop_range_80_84, pr.pop_range_85_89, pr.pop_range_90_94, pr.pop_range_95_99, pr.pop_range_100 from population_range pr join population_data pd on pd.pop_range_id = pr.pop_range_id join country c on c.country_id = pd.country_id"
df = pd.read_sql(query, engine)

app.layout = html.Div([
    dcc.Tabs(
        id='tabs',
        value='tab-report',
        children=[
            dcc.Tab(label='Home', value='tab-report'),
            dcc.Tab(label='US Data', value='tab-usa'),
            dcc.Tab(label='Population Data', value='tab-data'),
            dcc.Tab(label='Correlation Matrix', value='tab-matrix'), 
        ]
    ),
    html.Div(id='tabs-content')
])

# registers callbacks defined in callbacks file
register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True, dev_tools_props_check=False)
