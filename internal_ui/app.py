import streamlit as st
from google.cloud import firestore
import pandas as pd
import plotly.express as px
from datetime import date

st.title("Parking Pricing Dashboard")

db = firestore.Client()


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    docs = db.collection("listings").stream()
    rows = []
    for doc in docs:
        d = doc.to_dict()
        rows.append({
            "name": d.get("name"),
            "price_usd": d.get("price_usd"),
            "pricing_type": d.get("pricing_type"),
            "location": d.get("location"),
            "scraped_at": d.get("scraped_at"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["scraped_at"] = pd.to_datetime(df["scraped_at"], utc=True)
        df["date"] = df["scraped_at"].dt.date
        df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")
    return df


df = load_data()

if df.empty:
    st.warning("No data found in Firestore.")
    st.stop()

# Filters
with st.sidebar:
    st.header("Filters")
    selected_date = st.date_input(
        "Date",
        value=df["date"].max(),
        min_value=df["date"].min(),
        max_value=df["date"].max(),
    )
    locations = sorted(df["location"].dropna().unique())
    selected_location = st.selectbox("Location", locations)

    pricing_types = sorted(df["pricing_type"].dropna().unique())
    selected_type = st.selectbox("Pricing Type", pricing_types)

# Filter
filtered = df[
    (df["date"] == selected_date) &
    (df["location"] == selected_location) &
    (df["pricing_type"] == selected_type)
].dropna(subset=["price_usd"])

st.markdown(f"**{len(filtered)} listings** for {selected_location} on {selected_date} ({selected_type})")

if filtered.empty:
    st.info("No listings match the selected filters.")
else:
    fig = px.histogram(
        filtered,
        x="price_usd",
        title="Price Distribution (USD)",
        labels={"price_usd": "Price (USD)"},
    )
    fig.update_traces(xbins=dict(size=1))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(filtered[["name", "price_usd"]].sort_values("price_usd").reset_index(drop=True))
