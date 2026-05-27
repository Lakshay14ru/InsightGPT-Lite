import plotly.express as px

def create_histogram(df, column):
    fig = px.histogram(df, x=column)
    return fig

def create_scatter(df, x_col, y_col):
    fig = px.scatter(df, x=x_col, y=y_col)
    return fig