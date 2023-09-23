import datetime as dt
import requests

import numpy as np
import pandas as pd
import seaborn as sns


def get_gdp_per_capita(country, year):
    """
    Download GDP data.
    """
    alpha3 = {'Argentina': 'ARG', 'Canada': 'CAN',
              'Estonia': 'EST', 'Japan': 'JPN', 'Spain': 'ESP'}
    url = "https://api.worldbank.org/v2/country/{0}/indicator/NY.GDP.PCAP.CD?date={1}&format=json".format(
        alpha3[country], year)
    response = requests.get(url).json()
    return response[1][0]['value']


def gdp_countries(countries):
    gdp = []
    for country in countries:
        row = []
        for year in range(2017, 2023):
            row.append(get_gdp_per_capita(country, year))
        gdp.append(row)
        
    gdp = np.array(gdp)
    gdp /= np.sum(gdp) #to renomralize the data

    return gdp


def plot_data(axs, df, column, adj_column=None):
    """Helper function to plot insights."""
    for value in df[column].unique():
        value_data = df[df[column] == value]
        if not adj_column is None:
            value_data['num_sold'] = value_data['num_sold'] / value_data[adj_column]
        
        axs[0].plot(value_data['date'], value_data['num_sold'], ".", label=value)
        if adj_column is None:
            axs[1].plot(value_data['date'], value_data['num_sold'] /
                    value_data['num_sold'].sum(), ".", label=value)
            if len(axs) > 2:
                axs[2] = sns.kdeplot(value_data['num_sold']/value_data['num_sold'].sum(), label=value, ax=axs[2])
        else: 
            axs[1] = sns.kdeplot(value_data['num_sold']/value_data['num_sold'].sum(), label=value, ax=axs[1])

    for ax in axs:
        ax.legend()


def expand_time(df):
    """
    Create new features based on the available dates.
    """
    if not "date" in df.columns:
        raise TypeError("Expected dataframe with 'date' column.")
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear
    df['time_no'] = (
        df['date'] - dt.datetime(2017, 1, 1)) // dt.timedelta(days=1)
    df.loc[df['date'] > dt.datetime(2020, 2, 29), 'time_no'] -= 1
    date_columns = ['date', 'day', 'week', 'month', 'year', 'time_no']

    return df, date_columns
