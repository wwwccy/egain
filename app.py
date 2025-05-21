import streamlit as st
import pandas as pd

# Load sample data
data = {
    "ip_address": ["203.0.113.1", "198.51.100.7", "192.0.2.12"],
    "timestamp": ["2025-05-01 09:12:00", "2025-05-02 14:03:00", "2025-05-03 17:20:00"],
    "page_visited": ["/products/chatbot", "/pricing", "/contact"],
    "referrer": ["google.com", "linkedin.com", "direct"],
    "country": ["US", "UK", "CA"],
    "company": ["Acme Corp", "Beta Systems", "Nova Industries"],
    "page_views": [5, 3, 7]
}

df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)


st.title("🕵️ eGain Sales Intelligence Dashboard")


# Sidebar filters
st.sidebar.header("Filter Visitors")
company = st.sidebar.text_input("Company name")
country = st.sidebar.text_input("Country")
min_visits = st.sidebar.slider("Minimum page views", 1, 20, 1)

filtered_df = df.copy()

if company:
    filtered_df = filtered_df[filtered_df['company'].str.contains(company, case=False, na=False)]
if country:
    filtered_df = filtered_df[filtered_df['country'].str.contains(country, case=False, na=False)]

filtered_df = filtered_df[filtered_df['page_views'] >= min_visits]

st.subheader("🔍 Filtered Visitors")
st.dataframe(filtered_df)

st.subheader("📊 Page View Distribution")
st.bar_chart(filtered_df['page_views'])

st.subheader("🌍 Visitors by Country")
st.bar_chart(filtered_df['country'].value_counts())

