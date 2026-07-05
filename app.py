import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Used Car Analysis", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/car_data.csv")
    df["Car_Age"] = 2024 - df["Year"]
    df["Brand"] = df["Car_Name"].str.split().str[0].str.title()
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
fuel = st.sidebar.multiselect("Fuel Type", 
    options=["Petrol", "Diesel", "CNG"], 
    default=["Petrol", "Diesel", "CNG"])
transmission = st.sidebar.multiselect("Transmission", 
    options=["Manual", "Automatic"], 
    default=["Manual", "Automatic"])
year_range = st.sidebar.slider("Year Range", 
    min_value=2003, max_value=2018, value=(2003, 2018))

filtered = df[
    df["Fuel_Type"].isin(fuel) &
    df["Transmission"].isin(transmission) &
    df["Year"].between(year_range[0], year_range[1])
]

# Header
st.title("Used Car Market — India")
st.caption("Car Dekho dataset · EDA + Price Analysis")

# KPI cards
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Cars", len(filtered))
k2.metric("Avg Selling Price", f"₹{filtered['Selling_Price'].mean():.2f}L")
k3.metric("Avg Km Driven", f"{filtered['Kms_Driven'].mean():,.0f}")
k4.metric("Avg Car Age", f"{filtered['Car_Age'].mean():.1f} yrs")

st.divider()

# Row 1: Price distribution + Price by fuel type
c1, c2 = st.columns(2)

with c1:
    st.subheader("Selling Price Distribution")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.histplot(filtered["Selling_Price"], bins=25, kde=True, 
                 color="#1E3A5F", ax=ax)
    ax.set_xlabel("Selling Price (Lakhs)")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    plt.close()

with c2:
    st.subheader("Price by Fuel Type")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.boxplot(data=filtered, x="Fuel_Type", y="Selling_Price",
                hue="Fuel_Type", palette="Set2", legend=False, ax=ax)
    ax.set_xlabel("Fuel Type")
    ax.set_ylabel("Selling Price (Lakhs)")
    st.pyplot(fig)
    plt.close()

# Row 2: Km vs Price + Top brands
c3, c4 = st.columns(2)

with c3:
    st.subheader("Km Driven vs Selling Price")
    clean = filtered[filtered["Kms_Driven"] < 200000]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.scatterplot(data=clean, x="Kms_Driven", y="Selling_Price",
                    hue="Fuel_Type", alpha=0.7, ax=ax)
    ax.set_xlabel("Km Driven")
    ax.set_ylabel("Selling Price (Lakhs)")
    st.pyplot(fig)
    plt.close()

with c4:
    st.subheader("Top 10 Brands by Avg Resale Price")
    brand_avg = (filtered.groupby("Brand")["Selling_Price"]
                 .mean().sort_values(ascending=False).head(10))
    fig, ax = plt.subplots(figsize=(6, 3.5))
    brand_avg.plot(kind="bar", color="#D4470C", edgecolor="white", ax=ax)
    ax.set_ylabel("Avg Price (Lakhs)")
    ax.set_xlabel("")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)
    plt.close()

st.divider()

# Raw data
with st.expander("View raw data"):
    st.dataframe(filtered.reset_index(drop=True))