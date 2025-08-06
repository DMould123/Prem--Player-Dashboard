import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("premier_league_stats.csv")

st.title("Premier League Player Stats")

player = st.selectbox("Choose a player", df["Player"].unique())
player_data = df[df["Player"] == player]

st.write(player_data)

# Basic bar chart
fig, ax = plt.subplots()
ax.bar(["Goals", "Assists"], [player_data["Goals"].values[0],
       player_data["Assists"].values[0]])
st.pyplot(fig)
