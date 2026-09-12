import logging
import os

import pandas as pd
import plotly.express as px
from callbacks import Callbacks
from dash import Dash, Input, Output, dcc, html
from dynaconf import Dynaconf
from etl import (
    CountryETLProcessor,
    PopulationDataETLProcessor,
    PopulationRangeETLProcessor,
)
from graphing import BarGraphAnimated
from sqlalchemy import Engine, create_engine

os.chdir(os.path.dirname(__file__))

API_URL = "https://api.census.gov/data/timeseries/idb/5year"

def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
    return create_engine(settings.ENGINE_URL, echo=True)

def etl_processing(file_path: str, engine: Engine, countries: list[str]):

    country_etl = CountryETLProcessor(file_path=file_path, engine=engine, countries=countries)
    country_etl.process()

    population_range_etl = PopulationRangeETLProcessor(file_path=file_path, engine=engine, countries=countries)
    population_range_etl.process()

    population_data_etl = PopulationDataETLProcessor(file_path=file_path, engine=engine, countries=countries)
    population_data_etl.process()
    
def animated_bar_graph(df: pd.DataFrame):
    def years_with_all_countries(df):
        counts = (df.groupby('year')['country_name'].nunique().sort_index())
        n_countries = counts.max()
        first_full_year = counts[counts == n_countries].index.min()
        print(f"First year with all countries: {first_full_year}")

        filtered_df = df[df['year'] >= first_full_year]
        return filtered_df

    def max_range(df: pd.DataFrame, range_value: str):
        return df[range_value].max() * 1.1

    filtered_df = years_with_all_countries(df)

    max_pop = max_range(filtered_df, 'population_total')

    animated_bar_graph = BarGraphAnimated(
        df=filtered_df,
        x_value='country_name',
        y_value='population_total',
        color='country_name',
        animation_frame='year',
        animation_group='country_name',
        range_y=[0, max_pop]
    )

    return animated_bar_graph.bar_graph()


engine = build_engine()

# country_codes = ['W140000WOUS', 'W140000WOFR', 'W140000WOJP', 'W140000WOCN', 'W140000WODE', 'W140000WOIN', 'W140000WOCA', 'W140000WOMX', 'W140000WOAU', 'W140000WOIT']

# etl_processing(file_path="idbzip\\idb5yr.txt", engine=engine, countries=country_codes)

app = Dash(__name__)

query = "select c.country_name, pd.year, pd.population_total from population_data pd join country c on c.country_id = pd.country_id"
all_countries_df = pd.read_sql(query, engine)

query = "select c.country_name, pd.year, pd.population_total from population_data pd join country c on c.country_id = pd.country_id where c.country_name not in ('China', 'India', 'United States')"
small_countries_df = pd.read_sql(query, engine)

query = "select c.country_name, pd.year, pd.population_total from population_data pd join country c on c.country_id = pd.country_id where c.country_name in ('United States')"
us_df = pd.read_sql(query, engine)

query = "select c.country_name, pd.year, pd.population_total from population_data pd join country c on c.country_id = pd.country_id where c.country_name not in ('United States')"
not_us_df = pd.read_sql(query, engine)

# dash_display = DashDisplay(app, df, chart_type='line', chart_axes=('year', 'population_total'), df_grouping_col='country_name')

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='line-dropdown',
            options=[{'label': country, 'value': country} for country in sorted(all_countries_df['country_name'].unique())],
            multi=False,
            value=sorted(all_countries_df['country_name'].unique())[0]
        ),
        dcc.Graph(id='line-output'),
        # dcc.Graph(id='population-animated-graph', figure=countries_bar(small_countries_df))
        dcc.Graph(id='population-animated-graph', figure=animated_bar_graph(small_countries_df))
    ]
)

per_country_line = Callbacks(
    df=all_countries_df,
    app=app,
    output=Output("line-output", "figure"),
    input=Input("line-dropdown", "value"),
    x_axis='year',
    y_axis='population_total',
    df_grouping_col='country_name'
)
per_country_line.register_callbacks(per_country_line.update_line_graph)

if __name__ == "__main__":
    app.run(debug=True)