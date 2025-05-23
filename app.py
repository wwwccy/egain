import streamlit as st
import pandas as pd

# Load sample data
##data = {
##    "ip_address": ["203.0.113.1", "198.51.100.7", "192.0.2.12"],
##    "timestamp": ["2025-05-01 09:12:00", "2025-05-02 14:03:00", "2025-05-03 17:20:00"],
##    "page_visited": ["/products/chatbot", "/pricing", "/contact"],
##    "referrer": ["google.com", "linkedin.com", "direct"],
##    "location": ["US", "UK", "CA"],
##    "company": ["Acme Corp", "Beta Systems", "Nova Industries"],
##    "industry": ["Tech", "Tech", "Fin"],
##    "page_views": [5, 3, 7]
##}
##
##df = pd.DataFrame(data)
##df.to_csv("data.csv", index=False)

df = pd.read_csv('data.csv')
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.title("eGain Sales Intelligence Dashboard")


# Sidebar filters
st.sidebar.header("Filter Options")

# Time period filter
min_date = df["timestamp"].min().date()
max_date = df["timestamp"].max().date()
date_range = st.sidebar.date_input("Select date range", [min_date, max_date])
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]

company = st.sidebar.text_input("Company name")
location = st.sidebar.text_input("location")
industry = st.sidebar.text_input("industry")
page_visited = st.sidebar.text_input("page_visited")
min_visits = st.sidebar.slider("Minimum page views", 1, 20, 1)

filtered_df = df.copy()

if company:
    filtered_df = filtered_df[filtered_df['company'].str.contains(company, case=False, na=False)]
if location:
    filtered_df = filtered_df[filtered_df['location'].str.contains(location, case=False, na=False)]
if industry:
    filtered_df = filtered_df[filtered_df['industry'].str.contains(industry, case=False, na=False)]
if page_visited:
    filtered_df = filtered_df[filtered_df['page_visited'].str.contains(page_visited, case=False, na=False)]

filtered_df = filtered_df[filtered_df['page_views'] >= min_visits]

# Display filtered data
st.subheader("Filtered Visitor Logs")
st.dataframe(filtered_df)

st.subheader("Visitors by Company")
st.bar_chart(filtered_df['company'].value_counts())

st.subheader("Top Pages Visited")
st.bar_chart(filtered_df['page_visited'].value_counts())

# Summary stats
st.subheader("Summary Statistics")
st.write("Total Visits:", len(df))
st.write("Unique IPs:", df["ip_address"].nunique())
st.write("Top Companies:", df["company"].value_counts().head(5))
st.write("Top Industries:", df["industry"].value_counts().head(3))
