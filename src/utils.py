import datetime as dt
import requests

import holidays
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


def create_holiday(years, countries):
    """
    Utilize the holiday package to create holiday based information.
    """
    dfs = []
    # Generate holidays for each country and year
    for year in years:
        for country in countries:
            for date, holiday_name in sorted(holidays.CountryHoliday(country, years=year).items()):
                
                df_0 = pd.DataFrame({"date": [date], "country": [
                                country]})
                dfs.append(df_0)

    # Concatenate all the DataFrames
    df_holidays = pd.concat(dfs, ignore_index=True)

    # Convert 'date' column to datetime
    df_holidays['date'] = pd.to_datetime(df_holidays['date'])
    df_holidays['tmp'] = 1

    # remove certain holidays since the data doesn't have "holiday upturn" on these holidays
    df_holidays = df_holidays[~((df_holidays['date'].dt.month.isin([2,4,5,8,10])) & (df_holidays['country'] == 'Canada'))]
    # remove New Year and Christmas Holiday because I will handle them seperately
    for country in ['Argentina', 'Canada', 'Estonia', 'Spain']:
        for year in years:
            df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime(
                f'{year}-01-01')) & (df_holidays['country'] == country))]
    df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime(
        '2017-01-02')) & (df_holidays['country'] == 'Spain'))]

    for country in ['Argentina', 'Canada', 'Estonia', 'Spain']:
        for year in years:
            df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime(
                f'{year}-12-25')) & (df_holidays['country'] == country))]
    df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime(
        '2022-12-26')) & (df_holidays['country'] == 'Spain'))]

    # Canada and Estonia has additional holiday on 26th following Christmas. I will handle them separately
    for country in ['Canada', 'Estonia']:
        for year in years:
            df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime(
                f'{year}-12-26')) & (df_holidays['country'] == country))]

    #Canada has additional holiday on 27, 28. I remove them and it increases cross validation
    df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime('2020-12-28')) & (df_holidays['country'] == 'Canada'))]
    df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime('2021-12-27')) & (df_holidays['country'] == 'Canada'))]
    df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime('2021-12-28')) & (df_holidays['country'] == 'Canada'))]
    df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime('2022-12-27')) & (df_holidays['country'] == 'Canada'))]

    #it seems that Japan doesn't celebrate on this day. I remove it and it increases cross validation
    df_holidays = df_holidays[~((df_holidays['date'] == pd.to_datetime(
                f'2018-12-24')) & (df_holidays['country'] == 'Japan'))]
    
    return df_holidays