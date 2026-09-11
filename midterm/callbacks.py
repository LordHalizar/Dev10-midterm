from datetime import datetime

import pandas as pd
from dash import Input, Output
from graphing import HistogramOneSet, LineGraphOneSet, ScatterPlotOneSet


# function to validate if column info can be formatted as datetime
def is_valid_datetime(val_str, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(val_str, date_format)
        return True
    except ValueError:
        return False

# Callbacks class used to implement graphs in dash
class Callbacks:
    def __init__(
        self,
        df: pd.DataFrame,
        app,
        output: Output,
        input: Input,
        x_axis: str,
        y_axis: str | None = None,
        size: str | None = None,
        color: str | None = None,
        is_datetime: bool = False,
        df_grouping_col: str | None = None,
    ):
        self.df = df
        self.app = app
        self.output = output
        self.input = input
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.size = size
        self.color = color
        self.is_datetime = is_datetime
        self.df_grouping_col = df_grouping_col

    # Wrapper method for callbacks used to apply callback functionality to graphs
    def register_callbacks(self, callback_function):
        @self.app.callback(self.output, self.input)
        def callback_wrapper(selected_operation):
            return callback_function(selected_operation)

    # Update method used to generate scatter plot charts and update them based on selected operation by user
    def update_scatter_plot(self, selected_operation):
        x_col = self.x_axis
        if not selected_operation:
            selected_operation = self.y_axis

        y_col = selected_operation

        # Debugging line to test x-axis and y-axis parameter values
        # print(f"x-axis: {x_col}, y-axis: {y_col}")

        summarized_df = (
            self.df[[x_col, y_col, self.color]]
            .groupby([x_col, self.color], as_index=False)
            .mean()
            .reset_index()
        )

        scatter = ScatterPlotOneSet(
            df=summarized_df,
            x_value=x_col,
            y_value=y_col,
            title=f"Analysis of {y_col} per {x_col}",
            size=self.size,
            color=self.color
        )

        print(f"summarized df: \n{summarized_df.columns}")
        print(f"colors: \n{summarized_df[self.color].unique()}")

        return scatter.scatter_plot()

    # Update method used to generate histogram charts and update them based on selected operation by user
    def update_histogram(self, selected_operation):
        operations = {
            "count": lambda df: (
                df.groupby(self.x_axis).size().reset_index(name="Count")
            ),
            "sum": lambda df: df.groupby(self.x_axis, as_index=False)[
                self.y_axis
            ].sum(),
            "average": lambda df: df.groupby(self.x_axis, as_index=False)[
                self.y_axis
            ].mean(),
            "minimum": lambda df: df.groupby(self.x_axis, as_index=False)[
                self.y_axis
            ].min(),
            "maximum": lambda df: df.groupby(self.x_axis, as_index=False)[
                self.y_axis
            ].max(),
        }

        summarized_df = operations[selected_operation](self.df)

        x_col = self.x_axis
        y_col = "Count" if selected_operation == "count" else self.y_axis

        hist = HistogramOneSet(
            df=summarized_df,
            x_value=x_col,
            y_value=y_col,
            title=f"{selected_operation.title()} of {y_col} per {x_col}",
        )

        return hist.histogram()

    # Update method used to generate line graph charts and update them based on selected operation by user
    def update_line_graph(self, selected_operation):
        x_col = self.x_axis
        y_col = self.y_axis

        self.df = self.df.dropna(subset=[y_col])
        print(self.df.head())

        if self.is_datetime:
            valid_dates = self.df[x_col].astype(str).apply(is_valid_datetime)
            if valid_dates.all():
                self.df[x_col] = pd.to_datetime(self.df[x_col])

        # Debugging line to test x-axis and y-axis parameter values
        print(f"x-axis: {x_col}, y-axis: {y_col}")

        if self.df_grouping_col:
            selected_operation = (
                selected_operation[0]
                if isinstance(selected_operation, list)
                else selected_operation
            )
            print(f"selected operation: {selected_operation}")
            filtered_df = self.df[self.df[self.df_grouping_col] == selected_operation]
            print(f"filtered DataFrame: \n{filtered_df.head()}")
            summarized_df = (
                filtered_df.groupby([self.df_grouping_col, x_col])[y_col]
                .mean()
                .reset_index()
            )
        else:
            summarized_df = (
                self.df[[x_col] + [y_col]].groupby(x_col).mean().reset_index()
            )

        print(f"Summarized DataFrame: \n{summarized_df.head()}")

        line = LineGraphOneSet(
            df=summarized_df,
            x_value=x_col,
            y_value=y_col,
            title=f"Analysis of {y_col} by {x_col}",
        )

        return line.line_graph()