import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="Air Quality Analyzer", page_icon="🌬️", layout="wide")

st.title("🌬️ Air Quality Analyzer Dashboard")
st.write("Real-time visual comparison and safety monitoring of AQI across cities.")

# Sample Data
data = {
    'City': ['Mumbai', 'Delhi', 'Pune', 'Bangalore', 'Nagpur', 'Nashik'],
    'AQI': [160, 320, 95, 80, 110, 70]
}
df = pd.DataFrame(data)

# Sidebar Options
st.sidebar.header("Filter Options")
selected_city = st.sidebar.selectbox("Select a City:", df['City'])

# Display Selected City Metric
city_data = df[df['City'] == selected_city].iloc[0]
aqi_val = city_data['AQI']

col1, col2 = st.columns(2)

with col1:
    st.metric(label=f"Current AQI in {selected_city}", value=aqi_val)
    
    # Safety Alert
    if aqi_val <= 50:
        st.success("Air Quality is Good 🟢")
    elif aqi_val <= 100:
        st.warning("Air Quality is Moderate 🟡")
    elif aqi_val <= 200:
        st.error("Air Quality is Unhealthy for Sensitive Groups 🟠")
    else:
        st.error("Air Quality is Severe/Hazardous! 🔴")

with col2:
    # Interactive Plotly Chart
    fig = px.bar(df, x='City', y='AQI', color='AQI',
                 color_continuous_scale='Reds',
                 title="Overall City AQI Comparison")
    st.plotly_chart(fig, use_container_width=True)

