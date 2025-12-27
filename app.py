import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("premier_league_stats.csv")

st.title("Premier League Player Stats")

# Add team filter in sidebar
st.sidebar.header("Filters")
teams = ["All Teams"] + sorted(df["Team"].unique().tolist())
selected_team = st.sidebar.selectbox("Select Team", teams)

# Add position filter with specific order
position_order = ["GK", "DF", "MF", "FW"]
available_positions = [pos for pos in position_order if pos in df["Position"].unique()]
positions = ["All Positions"] + available_positions
selected_position = st.sidebar.selectbox("Select Position", positions)

# Filter dataframe by team and position
filtered_df = df.copy()

if selected_team != "All Teams":
    filtered_df = filtered_df[filtered_df["Team"] == selected_team]

if selected_position != "All Positions":
    filtered_df = filtered_df[filtered_df["Position"] == selected_position]

# Show filtered stats summary
st.sidebar.metric("Filtered Players", len(filtered_df))
if len(filtered_df) > 0:
    st.sidebar.metric("Total Goals", int(filtered_df["Goals"].sum()))
    st.sidebar.metric("Total Assists", int(filtered_df["Assists"].sum()))

# Add comparison mode toggle
st.sidebar.header("View Mode")
comparison_mode = st.sidebar.checkbox("Enable Player Comparison")

if comparison_mode:
    st.header("Compare Players")
    
    # Select multiple players
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("Player 1", filtered_df["Player"].unique(), key="p1")
        player1_data = filtered_df[filtered_df["Player"] == player1].iloc[0]
        
        st.subheader(player1)
        st.metric("Position", player1_data["Position"])
        st.metric("Team", player1_data["Team"])
        st.metric("Goals", int(player1_data["Goals"]))
        st.metric("Assists", int(player1_data["Assists"]))
        st.metric("Appearances", int(player1_data["Appearances"]))
        st.metric("Minutes", int(player1_data["Minutes"]))
    
    with col2:
        player2 = st.selectbox("Player 2", filtered_df["Player"].unique(), key="p2")
        player2_data = filtered_df[filtered_df["Player"] == player2].iloc[0]
        
        st.subheader(player2)
        st.metric("Position", player2_data["Position"])
        st.metric("Team", player2_data["Team"])
        st.metric("Goals", int(player2_data["Goals"]))
        st.metric("Assists", int(player2_data["Assists"]))
        st.metric("Appearances", int(player2_data["Appearances"]))
        st.metric("Minutes", int(player2_data["Minutes"]))
    
    # Comparison chart
    st.subheader("Side-by-Side Comparison")
    
    stats = ['Goals', 'Assists', 'Appearances', 'Minutes']
    player1_stats = [player1_data[stat] for stat in stats]
    player2_stats = [player2_data[stat] for stat in stats]
    
    # Normalize minutes for better visualization
    player1_stats_viz = player1_stats[:3] + [player1_stats[3]/100]
    player2_stats_viz = player2_stats[:3] + [player2_stats[3]/100]
    
    x = np.arange(len(stats))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, player1_stats_viz, width, label=player1, alpha=0.8)
    bars2 = ax.bar(x + width/2, player2_stats_viz, width, label=player2, alpha=0.8)
    
    ax.set_xlabel('Statistics')
    ax.set_ylabel('Value')
    ax.set_title(f'Player Comparison - {player1_data["Position"]} vs {player2_data["Position"]}')
    ax.set_xticks(x)
    ax.set_xticklabels(['Goals', 'Assists', 'Appearances', 'Minutes (x100)'])
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig)
    
    # Goals per game comparison
    st.subheader("Per Game Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**{player1}**")
        if player1_data["Appearances"] > 0:
            st.metric("Goals per Game", f"{player1_data['Goals']/player1_data['Appearances']:.2f}")
            st.metric("Assists per Game", f"{player1_data['Assists']/player1_data['Appearances']:.2f}")
    
    with col2:
        st.write(f"**{player2}**")
        if player2_data["Appearances"] > 0:
            st.metric("Goals per Game", f"{player2_data['Goals']/player2_data['Appearances']:.2f}")
            st.metric("Assists per Game", f"{player2_data['Assists']/player2_data['Appearances']:.2f}")

else:
    # Original single player view
    player = st.selectbox("Choose a player", filtered_df["Player"].unique())
    player_data = filtered_df[filtered_df["Player"] == player]

    # Display player info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Position", player_data["Position"].values[0])
    with col2:
        st.metric("Team", player_data["Team"].values[0])
    with col3:
        st.metric("Appearances", int(player_data["Appearances"].values[0]))
    with col4:
        st.metric("Minutes", int(player_data["Minutes"].values[0]))

    st.write(player_data)

    # Basic bar chart
    fig, ax = plt.subplots()
    ax.bar(["Goals", "Assists"], [int(player_data["Goals"].values[0]),
           int(player_data["Assists"].values[0])])
    ax.set_ylabel("Count")
    ax.set_title(f"{player}'s Goals and Assists ({player_data['Position'].values[0]})")
    st.pyplot(fig)
