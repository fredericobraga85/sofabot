import pandas as pd

def convert_to_timestamp(date):
    return pd.Timestamp(date).value / 1000000000


def convert_to_float(text):
    return float(text)

def convert_to_up_or_down(isUp):
    if isUp:
        return 1
    else:
        return -1

def convert_zero_to_none(value):
    if value == 0:
        return None

    return value