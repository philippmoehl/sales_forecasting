from pathlib import Path

import pandas as pd
import streamlit as st


BASE_PATH = Path.cwd()
DATA_PATH = BASE_PATH / "data"
TRAIN_PATH = DATA_PATH / "train.csv"


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(TRAIN_PATH, nrows=nrows, index_col="id")
    return data


@st.cache_data
def load_graph(column):
    df = pd.read_csv(TRAIN_PATH)
    df["date"] = pd.to_datetime(df['date'])
    
    grouped_data = df.groupby(['date', column])['num_sold'].sum().reset_index()

    dates = []
    num_sold = []
    colors = []

    for entry in df[column].unique():

        data_ = grouped_data[grouped_data[column] == entry]
        dates.extend(data_["date"])
        num_sold.extend(data_["num_sold"])
        colors.extend([entry] * len(data_["num_sold"]))
    

    data = pd.DataFrame(
        {
       "date": dates,
       "num_sold": num_sold,
       "color": colors,
        }
    )
        
    return data