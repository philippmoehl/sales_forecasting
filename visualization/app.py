import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

from utils import load_data, load_graph


# title
st.title("Sales Forecasting")

#description
st.write("Explore the sales dataset.")

# sidebar
sidebar = st.sidebar

# train or submission data
dataset = sidebar.radio(label="dataset", options=["train", "submission"])

# Display the dataframe
df_display = sidebar.checkbox("Display Raw Data", value=True)

if df_display:
    num_rows = sidebar.slider(
        "Select Number of rows",
        min_value=5,
        max_value=1000,
        value=5,
        step=5,
        
    )
    sales_data = load_data(dataset, num_rows)
    st.write(sales_data)

# display the line charts
category = sidebar.radio(label="category", options=["store", "country", "product"])
data_filt = load_graph(dataset, category)

st.line_chart(data_filt, x="date", y="num_sold", color="color")

# show prediction
