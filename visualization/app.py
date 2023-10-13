import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np

from utils import load_graph


BASE_PATH = Path.cwd()
DATA_PATH = BASE_PATH / "data"
TRAIN_PATH = DATA_PATH / "train.csv"
PRED_PATH = DATA_PATH / "prediction.csv"


# title
st.title("Sales Report 2017-2022")

# sidebar
sidebar = st.sidebar

# train or submission data
time_range = sidebar.radio(label="Time Range", options=["17_21", "17_22"])

# load data
train_data = pd.read_csv(TRAIN_PATH, index_col="id")
pred_data = pd.read_csv(PRED_PATH, index_col="id")

# sample some data
if sidebar.button("Show Sample"):
    st.write("Data sample")
    if time_range == "17_21":
        st.write(train_data.sample(5))
    else:
        st.write(pred_data.sample(5))

# display the line charts
category = sidebar.radio(label="category", options=["store", "country", "product"])
if time_range == "17_21":
    data_filt = load_graph("train", category)
else:
    data_filt = load_graph("prediction", category)

st.line_chart(data_filt, x="date", y="num_sold", color="color")