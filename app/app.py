import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt

import folium
from streamlit_folium import st_folium
from branca.colormap import linear

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# Load dataset
housing = fetch_california_housing(as_frame=True)
df = housing.frame
del housing

# Title
st.title("House Price dashboard")

# Plot 1: table of house prices
st.header("House Prices Data")
st.dataframe(df)

# Plot 2: scatter plot of house prices vs. median income
st.header("House Prices vs. Median Income")
plt.figure(figsize=(8,6))
plt.scatter(
    df["MedInc"], 
    df["MedHouseVal"],
    s=5
)
plt.xlabel("Median income")
plt.ylabel("Median house value")

st.pyplot(plt)

# Plot 3L: map of house prices and prediction
st.header("House Prices Map")

# Simple random forest model to predict house prices
X = df.drop(columns = "MedHouseVal")
y = df["MedHouseVal"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

# RF ML model, show interactive map
model_rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model_rf.fit(X_train, y_train)

# Predict on test set
test = X_test.copy()
test["actual"] = y_test
test["pred"] = model_rf.predict(X_test)
test["residual"] = test["actual"] - test["pred"]

print("R²:", r2_score(test["actual"], test["pred"]))

# 4) Sample points so the map stays fast (tweak as you like)
plot_df = test.sample(n=min(3000, len(test)), random_state=42).copy()

# 5) Create folium map centered on the sample
center = [plot_df["Latitude"].mean(), plot_df["Longitude"].mean()]
m = folium.Map(location=center, zoom_start=6, tiles="CartoDB positron")

# Choose what to colour by: "pred" or "residual"
color_by = "pred"  # change to "residual" to map errors instead

vmin, vmax = plot_df[color_by].min(), plot_df[color_by].max()
cmap = linear.viridis.scale(vmin, vmax)
cmap.caption = f"{color_by} (MedHouseVal in $100k units)" if color_by == "pred" else "Residual (actual - pred)"

# Layer: predicted values (or residuals)
fg = folium.FeatureGroup(name=f"Points coloured by {color_by}", show=True)

for _, r in plot_df.iterrows():
    val = float(r[color_by])
    folium.CircleMarker(
        location=[float(r["Latitude"]), float(r["Longitude"])],
        radius=3,
        weight=0,
        fill=True,
        fill_opacity=0.7,
        color=cmap(val),
        fill_color=cmap(val),
        tooltip=(
            f"Pred: {r['pred']:.2f} ($100k)<br>"
            f"Actual: {r['actual']:.2f} ($100k)<br>"
            f"Residual: {r['residual']:.2f}"
        ),
    ).add_to(fg)

fg.add_to(m)
cmap.add_to(m)
folium.LayerControl(collapsed=False).add_to(m)

# Display map in Streamlit
st_data = st_folium(m, width=700, height=500)
st.write(f"Random Forest Model R²: {r2_score(test['actual'], test['pred']):.4f}")