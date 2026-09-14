import pandas as pd
from graphing import BarGraphAnimated, LineGraph


# animated bar graph designed to display median age over time for all countries in data frame
def animated_median_age_bar_graph(df: pd.DataFrame):
    def years_with_all_countries(df):
        counts = df.groupby("year")["country_name"].nunique().sort_index()
        n_countries = counts.max()
        first_full_year = counts[counts == n_countries].index.min()
        # print(f"First year with all countries: {first_full_year}")

        filtered_df = df[df["year"] >= first_full_year]
        return filtered_df

    def max_range(df: pd.DataFrame, range_value: str):
        return df[range_value].max() * 1.1

    filtered_df = years_with_all_countries(df)

    max_pop = max_range(filtered_df, "median_age")

    animated_bar_graph = BarGraphAnimated(
        df=filtered_df,
        x_value="country_name",
        y_value="median_age",
        color="country_name",
        animation_frame="year",
        animation_group="country_name",
        range_y=[0, max_pop],
        labels={'median_age': 'Median Age', 'country_name': 'Country'},
        title="Comparative Analysis of Median Age over Time"
    )

    return animated_bar_graph.bar_graph()

# animated horizontal bar graph designed to display population age-ranges over time for one specific country
def animated_age_range_single_bar_graph(df: pd.DataFrame, country: str | None = None):
    df = df[df['country_name'] == country]

    def melt_df(df: pd.DataFrame):
        df_melted = df.melt(
            id_vars=["country_name", "year"],
            value_vars=[col for col in df.columns if "pop_range" in col],
            var_name="age_range",
            value_name="population",
        )
        return df_melted

    def max_range(df: pd.DataFrame, range_value: str):
        return df[range_value].max() * 1.1

    age_range_mapping = {
        "pop_range_0_4": "0-4 years",
        "pop_range_5_9": "5-9 years",
        "pop_range_10_14": "10-14 years",
        "pop_range_15_19": "15-19 years",
        "pop_range_20_24": "20-24 years",
        "pop_range_25_29": "25-29 years",
        "pop_range_30_34": "30-34 years",
        "pop_range_35_39": "35-39 years",
        "pop_range_40_44": "40-44 years",
        "pop_range_45_49": "45-49 years",
        "pop_range_50_54": "50-54 years",
        "pop_range_55_59": "55-59 years",
        "pop_range_60_64": "60-64 years",
        "pop_range_65_69": "65-69 years",
        "pop_range_70_74": "70-74 years",
        "pop_range_75_79": "75-79 years",
        "pop_range_80_84": "80-84 years",
        "pop_range_85_89": "85-89 years",
        "pop_range_90_94": "90-94 years",
        "pop_range_95_99": "95-99 years",
        "pop_range_100": "100+ years",
    }

    melted_df = melt_df(df)
    melted_df["age_range"] = melted_df["age_range"].replace(age_range_mapping)

    max_pop_range = max_range(melted_df, "population")

    animated_bar_graph = BarGraphAnimated(
        df=melted_df,
        x_value="population",
        y_value="age_range",
        orientation="h",
        color="age_range",
        animation_frame="year",
        title=f"Analysis of {country} Population Age Ranges Over Time",
        labels={"population": "Population", "age_range": "Age Range"},
        range_x=[0, max_pop_range],
    )

    return animated_bar_graph.bar_graph()

# correlation matrix designed to display correlation values between different columns/variables from the provided data frame.
def correlation_matrix(df: pd.DataFrame):
    if df.empty:
        raise ValueError("The input DataFrame is empty.")
    if not all(pd.api.types.is_numeric_dtype(df[col]) for col in df.columns):
        raise ValueError("All columns in the DataFrame must be numeric.")
    return df.corr()

def country_pop_line_graph(df: pd.DataFrame, country):
    country_df = df[df['country_name'] == country]

    line = LineGraph(
        df=country_df,
        x_value="year",
        y_value="population_total",
        title=f"Analysis of {country} Population Age Ranges Over Time",
        labels={"population_total": "Population", "year": "Year"},
    )

    return line.line_graph()