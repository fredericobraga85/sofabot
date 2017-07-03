import Converter
import pandas as pd

class ChartDataAnalyzer:

    def calculate_growth(self, series, index=1):
        return (series / series.shift(index) - 1) * 100

    def calculate_growth_1st_period(self, series):
        return (series / series[0] - 1) * 100

    def isUp(self, series, index=1):
        return (series > series.shift(index)).apply(Converter.convert_to_up_or_down)

    def run_feature_engineer(self, df):

        df['quoteVolume'] = df['quoteVolume'].apply(Converter.convert_to_float)
        df['timestamp'] = df['date'].apply(Converter.convert_to_timestamp)
        df['volumeGrowth'] = self.calculate_growth(df['volume'])
        df['quoteGrowth'] = self.calculate_growth(df['weightedAverage'])
        df['quoteGrowth1stPeriod'] = self.calculate_growth_1st_period(df['weightedAverage'])
        df['isUp'] = self.isUp(df['quoteGrowth1stPeriod'])

        return df

