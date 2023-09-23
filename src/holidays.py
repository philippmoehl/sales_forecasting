import datetime as dt

import holidays
import numpy as np
import pandas as pd


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


def calculate_holiday_diff():
    return [np.exp(-(i - 4.5) ** 2 / 8.5) for i in range(11)]

def add_holidays(df, df_holidays, holiday_diff):
    df['holiday'] = 0
    for day_no, diff in enumerate(holiday_diff):
        shifted = df_holidays.copy()
        shifted['date'] = shifted['date'] + dt.timedelta(days=day_no)
        df = pd.merge(df, shifted, on=['country', 'date'], how='left')
        df['tmp'].fillna(0, inplace=True)
        df['holiday'] += df['tmp'] * diff
        df.drop(columns='tmp', inplace=True)
    return df['holiday']


def add_special_dates(df):
    special_date_columns = []
    for day in range(25, 32):
        column = f'day_12_{day}'
        df[column] = ((df['month'] == 12) & (df['day'] == day) & (df['country'] != 'Japan')).astype(float)
        special_date_columns.append(column)

    for day in range(1, 11):
        column = f'day_1_{day}'
        df[column] = ((df['month'] == 1) & (df['day'] == day) & ((df['year'] == 2017) | (df['country'] != 'Japan'))).astype(float)
        special_date_columns.append(column)

    return special_date_columns

def add_custom_holidays(df, holiday_countries, column, holiday_diff):
    df[column] = 0
    for day_no, diff in enumerate(holiday_diff):
        df.loc[(df['country'].isin(holiday_countries)) & (df['month'] == 12) & (df['day'] == 26 + day_no), column] = diff
        df.loc[(df['country'].isin(holiday_countries)) & (df['month'] == 1) & (df['day'] == -5 + day_no), column] = diff