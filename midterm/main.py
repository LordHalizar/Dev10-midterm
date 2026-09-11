import logging
import os

import pandas as pd
from dynaconf import Dynaconf
from etl import (
    CountryETLProcessor,
    PopulationDataETLProcessor,
    PopulationRangeETLProcessor,
)
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

if __name__ == "__main__":

    engine = build_engine()

    country_codes = ['W140000WOUS', 'W140000WOFR', 'W140000WOJP', 'W140000WOCN', 'W140000WODE', 'W140000WOIN', 'W140000WOCA', 'W140000WOMX', 'W140000WOAU', 'W140000WOIT']

    etl_processing(file_path="idbzip\\idb5yr.txt", engine=engine, countries=country_codes)