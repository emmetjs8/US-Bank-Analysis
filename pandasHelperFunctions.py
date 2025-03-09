import pandas as pd

def seriesToTwoDimensionalList(series: pd.Series) -> list:
    """
    Converts a Pandas Series into a 2D list format where each row contains 
    a date (as a string) and the corresponding value.

    Args:
        series (pd.Series): The Pandas Series with dates as index and numeric values.

    Returns:
        list: A 2D list in the format [[date, value], ...].
    """
    return [[str(date)[0:10], value] for date, value in series.items()]