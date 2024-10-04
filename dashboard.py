import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for seaborn and matplotlib
sns.set(style="whitegrid")

# Helper functions for DataFrame creation
def create_daily_df(df):
    daily_df = df.groupby(by="dteday").agg({"cnt": "sum"}).reset_index()
    return daily_df

def create_users_df(df):
    total_casual_users = df["casual"].sum()
    total_registered_users = df["registered"].sum()
    user_type_df = {
        "Type of Users": ["Casual Users", "Registered Users"],
        "Users Total": [total_casual_users, total_registered_users],
    }
    return user_type_df

def create_year_df(df):
    year_df = df.groupby(by="yr").agg({"cnt": "sum"}).reset_index()
    return year_df

def create_season_df(df):
    season_df = df.groupby(by="season").agg({"cnt": "sum"}).reset_index()
    return season_df

def create_monthly_df(df):
    monthly_df = df.groupby(by="mnth").agg({"cnt": "sum"}).reset_index()
    return monthly_df

def create_hourly_df(df):
    hourly_df = df.groupby(by="hr").agg({"cnt": "sum"}).reset_index()
    return hourly_df

# Load datasets
all_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Date components
min_date = pd.to_datetime(all_df["dteday"]).dt.date.min()
max_date = pd.to_datetime(all_df["dteday"]).dt.date.max()

with st.sidebar:
    st.image(
        "logofix.png"
    )
    
    start_date, end_date = st.date_input(
        label="Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

main_df = all_df[
    (all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))
]

# Creating necessary DataFrames
daily_df = create_daily_df(main_df)
user_type_df = create_users_df(main_df)
year_df = create_year_df(main_df)
season_df = create_season_df(main_df)
monthly_df = create_monthly_df(main_df)
hourly_df = create_hourly_df(hour_df)

# Adding header with custom style for dark and brown theme
# Adding header
st.header(" ILMI'S BIKE RENTAL")

# Display total users and categories with icons
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("👤 Casual Users", value=int(main_df["casual"].sum()))
with col2:
    st.metric("👥 Registered Users", value=int(main_df["registered"].sum()))
with col3:
    st.metric("🌍 Total Users", value=int(main_df["cnt"].sum()))

# Monthly distribution
st.subheader("📅 Distribution of Bike Rentals by Month")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="mnth", y="cnt", data=monthly_df, palette="crest", ax=ax)
ax.set_title("Total Bike Rentals by Month", fontsize=16)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Total Rentals", fontsize=12)
st.pyplot(fig)

# Hourly distribution
st.subheader("🕒 Distribution of Bike Rentals by Hour")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x="hr", y="cnt", data=hourly_df, marker="o", color="orange", ax=ax, linewidth=2)
ax.set_title("Total Bike Rentals by Hour", fontsize=16)
ax.set_xlabel("Hour of Day", fontsize=12)
ax.set_ylabel("Total Rentals", fontsize=12)
st.pyplot(fig)

# Seasonal distribution
st.subheader("🍂 Distribution of Bike Rentals by Season")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="season", y="cnt", data=season_df, palette="viridis", ax=ax)
ax.set_title("Total Bike Rentals by Season", fontsize=16)
ax.set_xlabel("Season", fontsize=12)
ax.set_ylabel("Total Rentals", fontsize=12)
st.pyplot(fig)

# Add footer or any additional information
st.markdown("---")
st.write("Created by Ilmi Suciani Sinambela")

