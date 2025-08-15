import streamlit as st
import pandas as pd
import plotly.express as px

# 3. Load data
df = pd.read_csv("scraped_data.csv", parse_dates=["Date"])

# 4. Title
st.title("📈 Nigerian Exchange Rate Visualizer")
st.markdown("Use the sidebar to filter by year or select a specific date to explore NGN/USD exchange rates.")

# 5. Sidebar filter
st.sidebar.header("📅 Filter by Year")
min_year = df["Date"].dt.year.min()
max_year = df["Date"].dt.year.max()

start_year = st.sidebar.text_input("Start Year", str(min_year))
end_year = st.sidebar.text_input("End Year", str(max_year))
show_graph = st.sidebar.button("Show Graph")

# 6. Filtered Graph
if show_graph:
    st.markdown("### 📊 Filtered Exchange Rate Graph")

    try:
        start_date = pd.to_datetime(f"{start_year}-01-01")
        end_date = pd.to_datetime(f"{end_year}-12-31")
    except Exception as e:
        st.error(f"Invalid date format: {e}")
        st.stop()

    filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    if filtered.empty:
        st.warning("No data available for this date range.")
    else:
        fig = px.line(
            filtered,
            x='Date',
            y='ExchangeRate',
            title=f"Naira Exchange Rate ({start_year}–{end_year})",
            labels={'ExchangeRate': '₦/USD'},
            template='plotly_dark'
        )
        fig.update_traces(
            mode='lines+markers',
            line=dict(width=2),
            marker=dict(size=6),
            hovertemplate='Date: %{x|%Y-%m-%d}<br>Rate: ₦%{y:.2f}'
        )
        fig.update_xaxes(showgrid=True, gridcolor='gray')
        fig.update_yaxes(showgrid=True, gridcolor='gray')

        st.plotly_chart(fig, use_container_width=True)

# 7. Specific Date Checker (Sidebar)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Check Rate by Date")

specific_date = st.sidebar.date_input(
    "Pick a date",
    value=df["Date"].min(),
    min_value=df["Date"].min(),
    max_value=df["Date"].max(),
    key="specific_date"
)

show_rate = st.sidebar.button("Get rate for date")

# 8. Result Display on Main Page
if show_rate:
    specific_date = pd.to_datetime(specific_date)
    exact_row = df[df["Date"] == specific_date]

    st.markdown("### 📌 Exchange Rate Result")

    if exact_row.empty:
        closest = df.iloc[(df["Date"] - specific_date).abs().argsort()[:1]]
        st.info(
            f"No data for {specific_date.date()}. Closest: {closest.iloc[0]['Date'].date()} "
            f"— ₦{closest.iloc[0]['ExchangeRate']:.2f}/USD"
        )
    else:
        rate = exact_row.iloc[0]["ExchangeRate"]
        st.success(f"₦{rate:.2f}/USD on {specific_date.date()}")

