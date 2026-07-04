def filter_dataframe(df, column, values):
    return df[df[column].isin(values)]