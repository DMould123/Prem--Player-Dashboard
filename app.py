import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("premier_league_stats.csv")

# Calculate advanced statistics (per 90 minutes)
df["Goals_per_90"] = (df["Goals"] / df["Minutes"] * 90).round(2)
df["Assists_per_90"] = (df["Assists"] / df["Minutes"] * 90).round(2)
df["G+A_per_90"] = ((df["Goals"] + df["Assists"]) / df["Minutes"] * 90).round(2)

# Calculate efficiency metrics
df["Minutes_per_Goal"] = (df["Minutes"] / df["Goals"]).replace([np.inf, -np.inf], 0).round(0)
df["Minutes_per_Contribution"] = (df["Minutes"] / (df["Goals"] + df["Assists"])).replace([np.inf, -np.inf], 0).round(0)

# Replace NaN and inf values with 0
df = df.fillna(0)

st.title("Premier League Player Stats")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["🏠 Player Stats", "🏆 Leaderboards", "👥 Compare Players"])

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

# TAB 1: PLAYER STATS
with tab1:
    # Add search filter
    st.subheader("🔍 Search Player")
    search_term = st.text_input("Type player name to search", "").strip()
    
    # Filter players based on search term
    if search_term:
        search_filtered_df = filtered_df[filtered_df["Player"].str.contains(search_term, case=False, na=False)]
        if len(search_filtered_df) == 0:
            st.warning(f"No players found matching '{search_term}'")
            st.stop()
    else:
        search_filtered_df = filtered_df
    
    # Display number of matching players
    st.info(f"Found {len(search_filtered_df)} player(s)")
    
    # Player selection from search-filtered list
    player = st.selectbox("Choose a player", search_filtered_df["Player"].unique())
    player_data = search_filtered_df[search_filtered_df["Player"] == player].iloc[0]

    # Display player basic info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Position", player_data["Position"])
    with col2:
        st.metric("Team", player_data["Team"])
    with col3:
        st.metric("Appearances", int(player_data["Appearances"]))
    with col4:
        st.metric("Minutes", int(player_data["Minutes"]))
    
    # Display total stats
    st.subheader("📊 Season Totals")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Goals", int(player_data["Goals"]))
    with col2:
        st.metric("Assists", int(player_data["Assists"]))
    with col3:
        st.metric("Goal Contributions", int(player_data["Goals"] + player_data["Assists"]))
    
    # Display advanced stats (per 90 minutes)
    st.subheader("⚡ Per 90 Minutes")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Goals per 90", f"{player_data['Goals_per_90']:.2f}")
    with col2:
        st.metric("Assists per 90", f"{player_data['Assists_per_90']:.2f}")
    with col3:
        st.metric("G+A per 90", f"{player_data['G+A_per_90']:.2f}")
    
    # Display efficiency metrics
    st.subheader("🎯 Efficiency")
    col1, col2 = st.columns(2)
    with col1:
        mins_per_goal = player_data["Minutes_per_Goal"]
        if mins_per_goal > 0 and mins_per_goal != np.inf:
            st.metric("Minutes per Goal", f"{int(mins_per_goal)}")
        else:
            st.metric("Minutes per Goal", "N/A")
    with col2:
        mins_per_contrib = player_data["Minutes_per_Contribution"]
        if mins_per_contrib > 0 and mins_per_contrib != np.inf:
            st.metric("Minutes per Contribution", f"{int(mins_per_contrib)}")
        else:
            st.metric("Minutes per Contribution", "N/A")

    # Display full data table
    st.subheader("📋 Complete Stats")
    display_cols = ['Player', 'Team', 'Position', 'Goals', 'Assists', 'Appearances', 'Minutes', 
                    'Goals_per_90', 'Assists_per_90', 'G+A_per_90']
    st.dataframe(search_filtered_df[search_filtered_df["Player"] == player][display_cols], use_container_width=True)

    # Visualization - Goals vs Assists
    st.subheader("📈 Goals vs Assists")
    fig, ax = plt.subplots()
    ax.bar(["Goals", "Assists"], [int(player_data["Goals"]),
           int(player_data["Assists"])])
    ax.set_ylabel("Count")
    ax.set_title(f"{player}'s Goals and Assists ({player_data['Position']})")
    st.pyplot(fig)

# TAB 2: LEADERBOARDS
with tab2:
    st.header("🏆 Top Performers")
    
    # Top Goal Scorers
    st.subheader("⚽ Top 10 Goal Scorers")
    top_scorers = df.nlargest(10, 'Goals')[['Player', 'Team', 'Position', 'Goals', 'Appearances']]
    top_scorers['Goals/Game'] = (top_scorers['Goals'] / top_scorers['Appearances']).round(2)
    top_scorers.index = range(1, len(top_scorers) + 1)
    st.dataframe(top_scorers, use_container_width=True)
    
    # Top Assist Providers
    st.subheader("🎯 Top 10 Assist Providers")
    top_assisters = df.nlargest(10, 'Assists')[['Player', 'Team', 'Position', 'Assists', 'Appearances']]
    top_assisters['Assists/Game'] = (top_assisters['Assists'] / top_assisters['Appearances']).round(2)
    top_assisters.index = range(1, len(top_assisters) + 1)
    st.dataframe(top_assisters, use_container_width=True)
    
    # Combined Goals + Assists
    st.subheader("🌟 Top 10 Goal Contributions (Goals + Assists)")
    df['Total Contributions'] = df['Goals'] + df['Assists']
    top_contributors = df.nlargest(10, 'Total Contributions')[['Player', 'Team', 'Position', 'Goals', 'Assists', 'Total Contributions', 'Appearances']]
    top_contributors['Contributions/Game'] = (top_contributors['Total Contributions'] / top_contributors['Appearances']).round(2)
    top_contributors.index = range(1, len(top_contributors) + 1)
    st.dataframe(top_contributors, use_container_width=True)
    
    # Per 90 Minutes Leaderboards
    st.subheader("⚡ Top 10 by Per 90 Minutes (min. 500 minutes)")
    qualified_df = df[df['Minutes'] >= 500]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Goals per 90**")
        top_goals_per90 = qualified_df.nlargest(10, 'Goals_per_90')[['Player', 'Team', 'Position', 'Goals', 'Minutes', 'Goals_per_90']]
        top_goals_per90.index = range(1, len(top_goals_per90) + 1)
        st.dataframe(top_goals_per90, use_container_width=True)
    
    with col2:
        st.write("**G+A per 90**")
        top_ga_per90 = qualified_df.nlargest(10, 'G+A_per_90')[['Player', 'Team', 'Position', 'Goals', 'Assists', 'G+A_per_90']]
        top_ga_per90.index = range(1, len(top_ga_per90) + 1)
        st.dataframe(top_ga_per90, use_container_width=True)
    
    # Visualization
    st.subheader("📊 Top 5 Scorers vs Assisters")
    top5_scorers = df.nlargest(5, 'Goals')
    top5_assisters = df.nlargest(5, 'Assists')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Top Scorers Chart
    ax1.barh(top5_scorers['Player'], top5_scorers['Goals'], color='#FF6B6B')
    ax1.set_xlabel('Goals')
    ax1.set_title('Top 5 Goal Scorers')
    ax1.invert_yaxis()
    
    # Top Assisters Chart
    ax2.barh(top5_assisters['Player'], top5_assisters['Assists'], color='#4ECDC4')
    ax2.set_xlabel('Assists')
    ax2.set_title('Top 5 Assist Providers')
    ax2.invert_yaxis()
    
    plt.tight_layout()
    st.pyplot(fig)

# TAB 3: COMPARE PLAYERS
# TAB 3: COMPARE PLAYERS
with tab3:
    st.header("👥 Compare Players")
    
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
