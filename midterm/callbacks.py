import os

import pandas as pd
import plotly.graph_objs as go
from dash import Dash, Input, Output, dcc, html
from graphing import BarGraphAnimated, LineGraph
from graphs import (
    animated_age_range_single_bar_graph,
    animated_median_age_bar_graph,
    correlation_matrix,
    country_pop_line_graph,
)

os.chdir(os.path.dirname(__file__))

app = Dash(__name__)

# outer register callbacks function sets applied app and data frame for nested graph visualizations
def register_callbacks(app: Dash, df: pd.DataFrame):

    @app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
    )
    def render_content(tab):
        if tab == 'tab-intro':
            return html.Div([
                html.H3('Entity-Relationship Diagram'),
                html.Img(src=r'midterm\Entity-Relationship_Diagram.png', style={'width': '80%'})
            ])
        elif tab == 'tab-usa':
            return html.Div([
                html.H3('Country Data'),
                dcc.Graph(id='usa-line-graph', figure=country_pop_line_graph(df, 'United States')),
                dcc.Graph(id='usa-age-range', figure=animated_age_range_single_bar_graph(df, 'United States'),)
            ])
        elif tab == 'tab-data':
            return html.Div([
                html.H3('Population Data'),
                dcc.Dropdown(
                    id="line-dropdown-input",
                    options=[
                        {"label": country, "value": country}
                        for country in sorted(df["country_name"].unique())
                    ],
                    multi=True,
                    value=sorted(df["country_name"].unique())[0],
                ),
                dcc.Graph(id="line-dropdown-output"),
                dcc.Dropdown(
                    id="bar-dropdown-input",
                    options=[
                        {"label": country, "value": country}
                        for country in sorted(df["country_name"].unique())
                    ],
                    multi=False,
                    value=sorted(df["country_name"].unique())[0],
                ),
                dcc.Graph(id="bar-dropdown-output"),
                dcc.Graph(
                    id="population-animated-graph-median_ages",
                    figure=animated_median_age_bar_graph(df),
                ),
            ])
        elif tab == 'tab-matrix':
            correlation_df = df[['year', 'population_total', 'median_age', 'pop_range_0_4', 'pop_range_5_9', 'pop_range_10_14', 'pop_range_15_19', 'pop_range_20_24', 'pop_range_25_29', 'pop_range_30_34', 'pop_range_35_39', 'pop_range_40_44', 'pop_range_45_49', 'pop_range_50_54', 'pop_range_55_59', 'pop_range_60_64', 'pop_range_65_69', 'pop_range_70_74', 'pop_range_75_79', 'pop_range_80_84', 'pop_range_85_89', 'pop_range_90_94', 'pop_range_95_99', 'pop_range_100']]
            correlation_matrix_result = correlation_matrix(correlation_df)

            return html.Div([
                html.H3('Correlation Matrix'),
                dcc.Graph(
                    id="correlation-heatmap",
                    figure={
                        "data": [
                            go.Heatmap(
                                z=correlation_matrix_result.values,
                                x=correlation_matrix_result.columns,
                                y=correlation_matrix_result.columns,
                                colorscale="Viridis",
                                # colorscale='YlOrRd',
                                colorbar=dict(title="Correlation Coefficient"),
                            )
                        ],
                        "layout": go.Layout(
                            title="Correlation Matrix",
                            xaxis=dict(title="Variables"),
                            yaxis=dict(title="Variables"),
                            width=600,
                            height=600,
                        ),
                    },
                ),
            ])

    # line graph that displays population growth for selected countries from dropdown
    @app.callback(
        Output("line-dropdown-output", "figure"), Input("line-dropdown-input", "value")
    )
    def update_line_graph(selected_countries: list[str] | None = None):

        # applied fix to guarantee selection countries is list type 
        if not isinstance(selected_countries, list):
            selected_countries = [selected_countries] if selected_countries else []

        filtered_df = df[df["country_name"].isin(selected_countries)]

        # instantiation of custom line graph function from graphing classes
        fig = LineGraph(
            df=filtered_df,
            x_value="year",
            y_value="population_total",
            labels={"year": "Year", "population_total": "Population Total in MidYear"},
            hover_name="country_name",
            title="Comparative Analysis of Population Growth",
            color="country_name",
        )

        return fig.line_graph()

    # animated bar graph that displays age-range population stats for the selected country over time.
    @app.callback(
        Output("bar-dropdown-output", "figure"), Input("bar-dropdown-input", "value")
    )
    def animated_age_range_bar_graph(selected_country: str | None = None):
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

        # name mappings for age-range population data for easier naming conventions
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

        # filter data frame to only entries from user selected country
        filtered_df = melted_df[melted_df["country_name"] == selected_country]

        max_pop_range = max_range(filtered_df, "population")

        # Instantiation of custom graphing class of animated bar graphs
        animated_bar_graph = BarGraphAnimated(
            df=filtered_df,
            x_value="population",
            y_value="age_range",
            orientation="h",
            color="age_range",
            animation_frame="year",
            title=f"Analysis of {selected_country} Population Age Ranges Over Time",
            labels={"population": "Population", "age_range": "Age Range"},
            range_x=[0, max_pop_range],
        )

        return animated_bar_graph.bar_graph()
