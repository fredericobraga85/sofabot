import pandas as pd

def convert_to_timestamp(date):
    return pd.Timestamp(date).value / 1000000000


def convert_to_float(text):
    return float(text)