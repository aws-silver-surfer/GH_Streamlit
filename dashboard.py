import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
from pathlib import Path


#Plotting

import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st



st.title('Uber pickups in NYC')

#Define the working directory
dir_path = "../data"
#File names for import
revenue_file = Path(dir_path, "revenue_only.csv")
forecast_file = Path(dir_path, "forecast_country.csv")
all_data_file = Path(dir_path, "all_data.csv")
old_forecast_path =  "/Users/mhausch/Data/Prod_Dashboards/Data/volume_forecast_Q4_2023.csv"
new_forecast = "./data/volume_forecast_Q1_2024.csv"

#Read in data
old_forecast_import = pd.read_csv(old_forecast_path).fillna(0)
new_forecast_import = pd.read_csv(new_forecast).fillna(0)

forecast_perspective = "Product"

#Create the data for plotting

new_forecast_by_product = new_forecast_import.groupby([forecast_perspective])["Forecast_Value"].sum()
old_forecast_by_product = old_forecast_import.groupby([forecast_perspective])["Forecast_Value"].sum()
total_new_forecast = new_forecast_by_product.sum()
total_old_forecast = old_forecast_by_product.sum()
difference_forecasts = total_new_forecast - total_old_forecast
gap = pd.DataFrame()
gap["Difference"] = new_forecast_by_product - old_forecast_by_product
gap_list = gap["Difference"].to_list()
gap_list.insert(0,total_old_forecast)
temp_df = pd.Series(gap_list)
temp_df = temp_df.cumsum()
temp_df_2 = temp_df.diff().fillna(0)
result_list_final = temp_df_2.to_list()
# create the labels for the waterfall plot
lables_series = new_forecast_by_product.index.to_list()
lables_series.insert(0, "Old Forecast")
lables_series.append("Update forecast")
result_list_final.append(None)
st.title(result_list_final)
title = "Test"

gap.loc["New forecast"] = gap.Difference.sum()
gap = gap.reset_index()
df = pd.DataFrame(data = np.array([[0, 0]]),columns=["Product", "Difference"])
df.loc[0, "Product"] = "Last forecast"
data_df = pd.concat([df, gap], axis = 0)
labels = data_df["Product"].to_list()
values = data_df["Difference"].to_list()
fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = ["absolute", "relative", "relative", "relative","relative", "total"],
    x = labels,
    base = 0,
    y = values,
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
))

fig.update_layout(
        title = title,
        showlegend = True
)



st.plotly_chart(fig)