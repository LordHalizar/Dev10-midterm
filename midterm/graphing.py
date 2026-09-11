import pandas as pd
import plotly.express as px


# Validation check to make sure code users are calling correct child classes
def not_implemented_error():
    raise NotImplementedError("Subclasses should implement this method")

# Validation check to verify provided DataFrame isn't empty
def dataframe_validation(df):
    if df.empty:
        raise ValueError("The provided DataFrame is empty.")

# Base class and functionality for my scatter plot charts
class BaseScatterPlot:
    def __init__(
        self,
        df: pd.DataFrame,
        x_value: str,
        y_value: str,
        labels: dict | None = None,
        size: str | None = None,
        hover_name: str | None = None,
        title: str = "Scatter Plot",
        color: str | None = None
    ):
        self.df = df
        self.x_value = x_value
        self.y_value = y_value
        self.labels = labels
        self.size = size
        self.hover_name = hover_name
        self.title = title
        self.color = color

    def scatter_plot(self):
        not_implemented_error()

# Scatter plot graphing method meant to take in only one data set
class ScatterPlotOneSet(BaseScatterPlot):
    def scatter_plot(self):
        return px.scatter(
            data_frame=self.df,
            x=self.x_value,
            y=self.y_value,
            labels=self.labels,
            size=self.size,
            hover_name=self.hover_name,
            title=self.title,
            color=self.color
        )

# Base class and functionality for my histogram charts
class BaseHistogram:
    def __init__(
        self,
        df: pd.DataFrame,
        x_value: list[str],
        y_value: list[str],
        labels: dict | None = None,
        hover_name: str | None = None,
        title: str = "Histogram",
    ):
        self.df = df
        self.x_value = x_value
        self.y_value = y_value
        self.labels = labels
        self.hover_name = hover_name
        self.title = title

    def histogram(self):
        not_implemented_error()

# Histogram graphing method meant to take in only one data set
class HistogramOneSet(BaseHistogram):
    def histogram(self):
        return px.histogram(
            data_frame=self.df,
            x=self.x_value,
            y=self.y_value,
            labels=self.labels,
            hover_name=self.hover_name,
            title=self.title,
        )

# Base class and functionality for my line graph charts
class BaseLineGraph:
    def __init__(
        self,
        df: pd.DataFrame,
        x_value: str,
        y_value: str,
        labels: dict | None = None,
        hover_name: str | None = None,
        title: str = "Line Graph",
    ):
        self.df = df
        self.x_value = x_value
        self.y_value = y_value
        self.labels = labels
        self.hover_name = hover_name
        self.title = title

    def line_graph(self):
        not_implemented_error()

# Line graphing method meant to take in only one data set
class LineGraphOneSet(BaseLineGraph):
    def line_graph(self):
        return px.line(
            data_frame=self.df,
            x=self.x_value,
            y=self.y_value,
            labels=self.labels,
            hover_name=self.hover_name,
            title=self.title
        )