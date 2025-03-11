import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load Data
df_gdp = pd.read_csv("C:/Users/info/Downloads/gdp_actuals.csv", index_col="Date", parse_dates=True)
df_inflation = pd.read_csv("C:/Users/info/Downloads/inflation.csv", index_col="Date", parse_dates=True)

# Streamlit Layout
st.set_page_config(page_title="Macro Dashboard", layout="wide")
st.sidebar.title("📊 Macro Dashboard Settings")

# Sidebar: Indicator Selection
indicator = st.sidebar.selectbox("Select an Economic Indicator", ["GDP Growth", "Interest Rates", "Inflation"])

# Sidebar: Country Multi-Selection
available_countries = df_gdp.columns.tolist()
selected_countries = st.sidebar.multiselect("Select Countries", available_countries, default=["USA", "China"])

# Sidebar: Time Selection
start_year, end_year = st.sidebar.slider("Select Time Range", 2000, 2028, (2010, 2028))

# Fetch & Filter Data
df_selected = df_gdp[selected_countries]
df_selected_inflation= df_inflation[selected_countries]

df_selected = df_selected[(df_selected.index.year >= start_year) & (df_selected.index.year <= end_year)]
df_selected_inflation = df_selected_inflation[df_selected_inflation.index.year > 2024]

# Create Interactive Plot
fig = go.Figure()

for country in selected_countries:
    fig.add_trace(go.Scatter(x=df_selected.index, y=df_selected[country], mode="lines+markers", name=f"{country} (Actual)", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df_selected_inflation.index, y=df_selected_inflation[country], mode="lines+markers", name=f"{country} (Forecast)", line=dict(color="blue", dash="dash")))

fig.update_layout(title=f"{indicator} Over Time", xaxis_title="Year", yaxis_title=f"{indicator} (%)", plot_bgcolor="white")
st.plotly_chart(fig)

