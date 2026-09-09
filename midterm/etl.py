import logging

import pandas as pd


class BaseTransformer:
    def transform(self):
        raise NotImplementedError("Subclasses must implement the transform method for specific tables.")
    def _drop_na(self, df: pd.DataFrame, subset: list | None = None) -> pd.DataFrame:
        if subset:
            return df.dropna(subset=subset)
        return df.dropna()
    def _drop_duplicates(self, df: pd.DataFrame, subset: list | None = None) -> pd.DataFrame:
        if subset:
            return df.drop_duplicates(subset=subset)
        return df.drop_duplicates()

class CountryTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        us_df = df[df['GEO_ID'] == 'W140000WOUS']
        us_df = us_df.rename(columns={'GEO_ID': 'country_code'})
        us_df['country_code'] = us_df['country_code'].str[-2:]
        country_code_df = self._drop_duplicates(df=us_df, subset=['country_code'])
        country_code_df = country_code_df[['country_code']].reset_index(drop=True)
        return country_code_df

class PopulationRangeTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        range_variables = ["POP0_4", "POP5_9", "POP10_14", "POP15_19", "POP20_24", "POP25_29", "POP30_34", "POP35_39", "POP40_44", "POP45_49", "POP50_54", "POP55_59", "POP60_64", "POP65_69", "POP70_74", "POP75_79", "POP80_84", "POP85_89", "POP90_94", "POP95_99", "POP100_"]
        us_df = df[df['GEO_ID'] == 'W140000WOUS']
        range_df = us_df[range_variables]
        range_df = self._drop_na(range_df, subset=range_variables)

        rename_mapping = {
            "POP0_4": "pop_range_0_4",
            "POP5_9": "pop_range_5_9",
            "POP10_14": "pop_range_10_14",
            "POP15_19": "pop_range_15_19",
            "POP20_24": "pop_range_20_24",
            "POP25_29": "pop_range_25_29",
            "POP30_34": "pop_range_30_34",
            "POP35_39": "pop_range_35_39",
            "POP40_44": "pop_range_40_44",
            "POP45_49": "pop_range_45_49",
            "POP50_54": "pop_range_50_54",
            "POP55_59": "pop_range_55_59",
            "POP60_64": "pop_range_60_64",
            "POP65_69": "pop_range_65_69",
            "POP70_74": "pop_range_70_74",
            "POP75_79": "pop_range_75_79",
            "POP80_84": "pop_range_80_84",
            "POP85_89": "pop_range_85_89",
            "POP90_94": "pop_range_90_94",
            "POP95_99": "pop_range_95_99",
            "POP100_": "pop_range_100"
        }

        range_df = range_df.rename(columns=rename_mapping)

        # range_df = self._drop_duplicates(range_df, subset=range_variables)
        return range_df

class PopulationRateTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        rate_variables = ["E0", "IMR", "RNI"]

        us_df = df[df['GEO_ID'] == 'W140000WOUS']
        rate_df = us_df[rate_variables]

        rename_mapping = {
            "E0": "life_expectancy",
            "IMR": "infant_mortality",
            "RNI": "natural_rate"
        }

        rate_df = rate_df.rename(columns=rename_mapping)
        rate_df = self._drop_na(rate_df, subset=["life_expectancy", "infant_mortality", "natural_rate"])

        return rate_df

class PopulationDataTransformer(BaseTransformer):
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        data_variables = ["#YR", "MEDAGE"]

        us_df = df[df['GEO_ID'] == 'W140000WOUS']
        data_df = us_df[data_variables]

        rename_mapping = {
            "#YR": "year",
            "MEDAGE": "median_age"
        }
        
class BaseETLProcessor:
    def __init__(self, file_path, engine, transformer, table_name):
        self.file_path = file_path
        self.engine = engine
        self.transformer = transformer
        self.table_name = table_name
    def extract(self):
        raise NotImplementedError("Subclasses must implement the etl class for specific table types.")
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.transformer.transform(df)
    def load(self, df: pd.DataFrame) -> pd.DataFrame:
        df.to_sql(name=self.table_name, con=self.engine, if_exists="append", index=False)


class CountryETLProcessor(BaseETLProcessor):
    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, delimiter="|")
    def process(self):
        print("Extracting data for country table...")
        txt_df = self.extract()

        print("Transforming data for country table...")
        transformed_df = self.transform(txt_df)
        print(transformed_df)

        try:
            print("Loading country table data...")
            self.load(transformed_df)
        except pd.errors.DatabaseError as e:
            print(f"[ERR]: {e}")

class PopulationRangeETLProcessor(BaseETLProcessor):
    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, delimiter="|")
    def process(self):
        print("Extracting data for population range table...")
        txt_df = self.extract()

        print("Transforming data for population range table...")
        transformed_df = self.transform(txt_df)
        print(transformed_df)

        try:
            print("Loading population range table data...")
            self.load(transformed_df)
        except pd.errors.DatabaseError as e:
            print(f"[ERR]: {e}")

class PopulationRateETLProcessor(BaseETLProcessor):
    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, delimiter="|")
    def process(self):
        print("Extracting data for population rate table...")
        txt_df = self.extract()

        print("Transforming data for population rate table...")
        transformed_df = self.transform(txt_df)
        print(transformed_df)

        try:
            print("Loading population rate table data...")
            self.load(transformed_df)
        except pd.errors.DatabaseError as e:
            print(f"[ERR]: {e}")