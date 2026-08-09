import plotly.express as px

def create_histogram(df, column):
    fig = px.histogram(df, x=column)
    return fig

def create_scatter(df, x_col, y_col):
    fig = px.scatter(df, x=x_col, y=y_col)
    return fig

def create_box_plot(df, column):

    import plotly.express as px

    fig = px.box(
        df,
        y=column,
        title=f"Box Plot - {column}"
    )

    return fig

def create_bar_chart(df, column):

    import plotly.express as px

    value_counts = df[column].value_counts().reset_index()

    value_counts.columns = [column, "Count"]

    fig = px.bar(
        value_counts,
        x=column,
        y="Count",
        title=f"Bar Chart - {column}"
    )

    return fig

def create_pie_chart(df, column):

    import plotly.express as px

    value_counts = df[column].value_counts().reset_index()

    value_counts.columns = [column, "Count"]

    fig = px.pie(
        value_counts,
        names=column,
        values="Count",
        title=f"Distribution of {column}"
    )

    return fig

def create_line_chart(df, x_column, y_column):

    import plotly.express as px

    fig = px.line(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} vs {x_column}"
    )

    return fig