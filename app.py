import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("premier_league_stats.csv")

st.title("Premier League Player Stats")

# Add team filter in sidebar
st.sidebar.header("Filters")
teams = ["All Teams"] + sorted(df["Team"].unique().tolist())
selected_team = st.sidebar.selectbox("Select Team", teams)

# Filter dataframe by team
if selected_team != "All Teams":
    filtered_df = df[df["Team"] == selected_team]
else:
    filtered_df = df

# Show team stats summary
if selected_team != "All Teams":
    st.sidebar.metric("Total Players", len(filtered_df))
    st.sidebar.metric("Total Goals", filtered_df["Goals"].sum())
    st.sidebar.metric("Total Assists", filtered_df["Assists"].sum())

# Player selection from filtered list
player = st.selectbox("Choose a player", filtered_df["Player"].unique())
player_data = filtered_df[filtered_df["Player"] == player]

# Display player info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Team", player_data["Team"].values[0])
with col2:
    st.metric("Appearances", player_data["Appearances"].values[0])
with col3:
    st.metric("Minutes", player_data["Minutes"].values[0])

st.write(player_data)

# Basic bar chart
fig, ax = plt.subplots()
ax.bar(["Goals", "Assists"], [player_data["Goals"].values[0],
       player_data["Assists"].values[0]])
ax.set_ylabel("Count")
ax.set_title(f"{player}'s Goals and Assists")
st.pyplot(fig)
