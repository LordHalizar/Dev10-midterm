import logging
import os

import pandas as pd
from dynaconf import Dynaconf
from etl import CountryTransformer, ETLProcessor, PopulationRangeTransformer, PopulationRateTransformer
from sqlalchemy import create_engine

os.chdir(os.path.dirname(__file__))

API_URL = "https://api.census.gov/data/timeseries/idb/5year"

def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
    return create_engine(settings.ENGINE_URL, echo=True)

def run():
    engine = build_engine()


if __name__ == "__main__":

    engine = build_engine()

    # data_variables = ["POP0_4", "POP5_9", "POP10_14", "POP15_19", "POP20_24", "POP25_29", "POP30_34", "POP35_39", "POP40_44", "POP45_49", "POP50_54", "POP55_59", "POP60_64", "POP65_69", "POP70_74", "POP75_79", "POP80_84", "POP85_89", "POP90_94", "POP95_99", "POP100_"]

    country_etl = ETLProcessor(file_path="idbzip\\idb5yr.txt", engine=engine, transformer=CountryTransformer(), table_name="country")
    country_etl.process()

    range_etl = ETLProcessor(file_path="idbzip\\idb5yr.txt", engine=engine, transformer=PopulationRangeTransformer(), table_name="population_range")
    range_etl.process()

    rate_etl = ETLProcessor(file_path="idbzip\\idb5yr.txt", engine=engine, transformer=PopulationRateTransformer(), table_name="population_rate")
    rate_etl.process()