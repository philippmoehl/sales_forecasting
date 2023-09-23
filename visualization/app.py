import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt



@st.cache_data
def load_data(nrows):
    data = pd.read_csv('data/train.csv', nrows=nrows)
    return data


@st.cache_data
def load_graph(column):
    df = pd.read_csv('data/train.csv')
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


# title
st.title("Sales Forecasting")

#description
st.write("Here is the dataset used in this analysis:")


# Display the dataframe
df_display = st.checkbox("Display Raw Data", value=True)

if df_display:
    num_rows = st.slider(
        "Select Number of rows",
        min_value=10,
        max_value=100,
        value=10,
        step=10,
        
    )
    sales_data = load_data(num_rows)
    st.write(sales_data)


category = st.radio(label="category", options=["store", "country", "product"])
data_filt = load_graph(category)

st.line_chart(data_filt, x="date", y="num_sold", color="color")
