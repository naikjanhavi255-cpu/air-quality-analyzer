import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.title("Air Quality Analyzer")

data = {
    "City": ["Mumbai", "Delhi", "Pune", "Bangalore"],
    "AQI": [160, 320, 95, 80]
}
df = pd.DataFrame(data)

st.subheader("AQI Comparison")
fig, ax = plt.subplots()
sns.barplot(x="City", y="AQI", data=df, ax=ax)
st.pyplot(fig)
