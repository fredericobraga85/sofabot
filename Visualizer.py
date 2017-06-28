import pandas as pd


def print_full(x):
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')