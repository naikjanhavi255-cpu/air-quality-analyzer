import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Air Quality Analyzer",
    page_icon="🌍",
    layout="wide"
)

# Title & Subtitle
st.title("🌍 Air Quality Analyzer Dashboard")
st.write("Upload air-quality data to explore pollutant trends, correlations, and hour-wise heatmaps.")

# -------------------------
# Upload data or Load Default
# -------------------------
uploaded_file = st.sidebar.file_uploader("Upload an air-quality CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("air_quality.csv")
        st.sidebar.info("Using default dataset (`air_quality.csv`). Upload your own CSV anytime!")
    except FileNotFoundError:
        st.error("Please upload a CSV file to proceed.")
        st.stop()

# -------------------------
# Convert Datetime
# -------------------------
if "datetime" in df.columns:
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime"]).sort_values("datetime")

# -------------------------
# Sidebar - Filters
# -------------------------
st.sidebar.header("Filter Options")

# Date range selector
if "datetime" in df.columns:
    min_date = df["datetime"].dt.date.min()
    max_date = df["datetime"].dt.date.max()
    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)
    
    # Filter DataFrame
    df = df[(df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)]

# Find pollutant columns
pollutants = [col for col in ["PM2.5", "PM10", "NO2", "CO"] if col in df.columns]

if not pollutants:
    st.error("No recognized pollutant columns found in CSV.")
    st.stop()

selected_pollutant = st.sidebar.selectbox("Select Main Pollutant", pollutants)

# -------------------------
# Summary Metrics
# -------------------------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Concentration", f"{df[selected_pollutant].mean():.2f}")
col2.metric("Maximum Concentration", f"{df[selected_pollutant].max():.2f}")
col3.metric("Minimum Concentration", f"{df[selected_pollutant].min():.2f}")

# -------------------------
# Visualizations
# -------------------------
st.divider()

# 1. Time-series Line Chart
st.subheader(f"📈 {selected_pollutant} Concentration Over Time")
fig_line = px.line(df, x="datetime", y=selected_pollutant, title=f"{selected_pollutant} Trend")
st.plotly_chart(fig_line, use_container_width=True)

# 2. Pollutant Comparison
st.subheader("🧪 Pollutant Comparison")
selected_multi = st.multiselect("Select pollutants to compare:", pollutants, default=pollutants[:2])
if selected_multi:
    fig_comp = px.line(df, x="datetime", y=selected_multi, title="Pollutants Trend Comparison")
    st.plotly_chart(fig_comp, use_container_width=True)

# 3. Correlation Matrix & Scatter Plot
col_a, col_b = st.columns(2)

with col_a:
    if "humidity" in df.columns and selected_pollutant in df.columns:
        st.subheader("💧 Humidity vs Pollutant")
        fig_scatter = px.scatter(df, x="humidity", y=selected_pollutant, trendline="ols", title=f"Humidity vs {selected_pollutant}")
        st.plotly_chart(fig_scatter, use_container_width=True)

with col_b:
    st.subheader("🔥 Pollution Heatmap (Hour vs Date)")
    if "datetime" in df.columns:
        df["date"] = df["datetime"].dt.date
        df["hour"] = df["datetime"].dt.hour
        heatmap_data = df.pivot_table(values=selected_pollutant, index="hour", columns="date", aggfunc="mean")
        fig_heat = px.imshow(heatmap_data, labels={"x": "Date", "y": "Hour", "color": selected_pollutant})
        st.plotly_chart(fig_heat, use_container_width=True)

# Raw Data View
with st.expander("📁 View Filtered Dataset"):
    st.dataframe(df, use_container_width=True)


