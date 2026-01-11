import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page config
st.set_page_config(page_title="Premier League Dashboard", page_icon="⚽", layout="wide")

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

# Header
st.markdown("# ⚽ Premier League Dashboard")
st.markdown("### 2024-25 Season Player Statistics")
st.markdown("---")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 Player Stats", "🏆 Leaderboards", "⚖️ Compare Players"])

# Sidebar with better styling
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 24px;'>⚽ PL STATS</h2>
            <p style='color: #e0e0e0; margin: 5px 0 0 0; font-size: 12px;'>Premier League Analytics</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🎯 Filters")
    st.markdown("")
    
    # Team filter
    teams = ["All Teams"] + sorted(df["Team"].unique().tolist())
    selected_team = st.selectbox("⚽ Team", teams)
    
    # Position filter with specific order
    position_order = ["GK", "DF", "MF", "FW"]
    available_positions = [pos for pos in position_order if pos in df["Position"].unique()]
    positions = ["All Positions"] + available_positions
    selected_position = st.selectbox("📍 Position", positions)
    
    st.markdown("---")
    
    # Filter dataframe by team and position
    filtered_df = df.copy()
    
    if selected_team != "All Teams":
        filtered_df = filtered_df[filtered_df["Team"] == selected_team]
    
    if selected_position != "All Positions":
        filtered_df = filtered_df[filtered_df["Position"] == selected_position]
    
    # Show filtered stats summary with better formatting
    st.markdown("### 📈 Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Players", len(filtered_df))
    with col2:
        st.metric("Teams", filtered_df["Team"].nunique())
    
    if len(filtered_df) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Goals", int(filtered_df["Goals"].sum()))
        with col2:
            st.metric("Assists", int(filtered_df["Assists"].sum()))
    
    st.markdown("---")
    st.markdown("**Data Source:** FBref via Kaggle")
    st.markdown("**Season:** 2024-25")

# TAB 1: PLAYER STATS
with tab1:
    # Search bar with better styling
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("🔍 Search for a player", "", placeholder="e.g., Haaland, Salah, De Bruyne...").strip()
    
    # Filter players based on search term
    if search_term:
        search_filtered_df = filtered_df[filtered_df["Player"].str.contains(search_term, case=False, na=False)]
        if len(search_filtered_df) == 0:
            st.error(f"❌ No players found matching '{search_term}'")
            st.stop()
    else:
        search_filtered_df = filtered_df
    
    with col2:
        st.metric("📋 Results", len(search_filtered_df))
    
    st.markdown("")
    
    # Player selection
    player = st.selectbox("Select a player to view detailed stats", search_filtered_df["Player"].unique(), label_visibility="collapsed")
    player_data = search_filtered_df[search_filtered_df["Player"] == player].iloc[0]

    st.markdown("")
    
    # Player Card Header
    st.markdown(f"# {player}")
    
    # Player info in a clean card-style layout
    info_col1, info_col2, info_col3, info_col4 = st.columns(4)
    with info_col1:
        st.markdown(f"**🎽 Position**")
        st.markdown(f"### {player_data['Position']}")
    with info_col2:
        st.markdown(f"**⚽ Team**")
        st.markdown(f"### {player_data['Team']}")
    with info_col3:
        st.markdown(f"**🌍 Nation**")
        st.markdown(f"### {player_data['Nationality']}")
    with info_col4:
        st.markdown(f"**📅 Age**")
        st.markdown(f"### {int(player_data['Age'])}")
    
    st.markdown("---")
    
    # Key metrics row
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    with metric_col1:
        st.metric("🏃 Appearances", int(player_data["Appearances"]))
    with metric_col2:
        st.metric("⏱️ Minutes", int(player_data["Minutes"]))
    with metric_col3:
        if player_data["Appearances"] > 0:
            avg_mins = int(player_data["Minutes"] / player_data["Appearances"])
            st.metric("📊 Mins/Game", avg_mins)
        else:
            st.metric("📊 Mins/Game", "N/A")
    with metric_col4:
        if player_data["Position"] != "GK":
            st.metric("🎯 G+A", int(player_data["Goals"] + player_data["Assists"]))
        else:
            if 'Clean_Sheets' in player_data.index and player_data["Clean_Sheets"] > 0:
                st.metric("🧤 Clean Sheets", int(player_data["Clean_Sheets"]))
            else:
                st.metric("🧤 Clean Sheets", "N/A")
    
    st.markdown("")
    
    # Check if player is a goalkeeper
    is_goalkeeper = player_data["Position"] == "GK"
    
    if is_goalkeeper:
        # GOALKEEPER LAYOUT
        has_gk_stats = 'Clean_Sheets' in player_data.index and pd.notna(player_data["Clean_Sheets"])
        
        if has_gk_stats:
            # Two column layout for GK
            left_col, right_col = st.columns([1, 1])
            
            with left_col:
                st.markdown("### 🧤 Goalkeeper Performance")
                
                perf_col1, perf_col2 = st.columns(2)
                with perf_col1:
                    st.metric("Clean Sheets", int(player_data["Clean_Sheets"]))
                    clean_sheet_pct = (player_data["Clean_Sheets"] / player_data["Appearances"] * 100) if player_data["Appearances"] > 0 else 0
                    st.metric("Clean Sheet %", f"{clean_sheet_pct:.1f}%")
                with perf_col2:
                    st.metric("Goals Conceded", int(player_data["Goals_Against"]))
                    goals_per_game = player_data["Goals_Against"] / player_data["Appearances"] if player_data["Appearances"] > 0 else 0
                    st.metric("Conceded/Game", f"{goals_per_game:.2f}")
                
                st.markdown("")
                
                if 'Save_Percentage' in player_data.index and player_data["Save_Percentage"] > 0:
                    st.metric("💪 Save Percentage", f"{player_data['Save_Percentage']:.1f}%")
            
            with right_col:
                st.markdown("### 📊 Performance Chart")
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(["Clean Sheets", "Goals Conceded"], 
                       [int(player_data["Clean_Sheets"]), int(player_data["Goals_Against"])],
                       color=['#2ecc71', '#e74c3c'])
                ax.set_ylabel("Count", fontsize=11)
                ax.grid(axis='y', alpha=0.3)
                st.pyplot(fig)
        else:
            st.info("⚠️ Detailed goalkeeper stats not available for this player")
    
    else:
        # OUTFIELD PLAYER LAYOUT
        is_midfielder = player_data["Position"] == "MF"
        
        # Main stats in two columns
        left_col, right_col = st.columns([1, 1])
        
        with left_col:
            st.markdown("### ⚽ Attacking Stats")
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Goals", int(player_data["Goals"]))
            with stat_col2:
                st.metric("Assists", int(player_data["Assists"]))
            with stat_col3:
                st.metric("G+A", int(player_data["Goals"] + player_data["Assists"]))
            
            st.markdown("")
            
            # Per 90 stats
            st.markdown("**📈 Per 90 Minutes**")
            per90_col1, per90_col2, per90_col3 = st.columns(3)
            with per90_col1:
                st.metric("G/90", f"{player_data['Goals_per_90']:.2f}")
            with per90_col2:
                st.metric("A/90", f"{player_data['Assists_per_90']:.2f}")
            with per90_col3:
                st.metric("G+A/90", f"{player_data['G+A_per_90']:.2f}")
        
        with right_col:
            st.markdown("### 📊 Performance Chart")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(["Goals", "Assists"], [int(player_data["Goals"]), int(player_data["Assists"])],
                   color=['#e74c3c', '#3498db'])
            ax.set_ylabel("Count", fontsize=11)
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        st.markdown("")
        
        # Midfielder-specific stats in expandable section
        if is_midfielder and 'xG' in player_data.index and player_data['Progressive_Passes'] > 0:
            with st.expander("🎯 **Advanced Midfielder Stats**", expanded=False):
                adv_col1, adv_col2, adv_col3 = st.columns(3)
                
                with adv_col1:
                    st.markdown("**Expected Stats**")
                    st.metric("xG", f"{player_data['xG']:.1f}")
                    st.metric("xAG", f"{player_data['xAG']:.1f}")
                
                with adv_col2:
                    st.markdown("**Passing & Carries**")
                    st.metric("Progressive Passes", int(player_data["Progressive_Passes"]))
                    st.metric("Progressive Carries", int(player_data["Progressive_Carries"]))
                
                with adv_col3:
                    st.markdown("**Receptions**")
                    st.metric("Progressive Receptions", int(player_data["Progressive_Receptions"]))
        
        # Efficiency metrics in expandable section
        with st.expander("⚡ **Efficiency Metrics**", expanded=False):
            eff_col1, eff_col2 = st.columns(2)
            with eff_col1:
                mins_per_goal = player_data["Minutes_per_Goal"]
                if mins_per_goal > 0 and mins_per_goal != np.inf:
                    st.metric("⏱️ Minutes per Goal", f"{int(mins_per_goal)}")
                else:
                    st.metric("⏱️ Minutes per Goal", "N/A")
            with eff_col2:
                mins_per_contrib = player_data["Minutes_per_Contribution"]
                if mins_per_contrib > 0 and mins_per_contrib != np.inf:
                    st.metric("⏱️ Minutes per Contribution", f"{int(mins_per_contrib)}")
                else:
                    st.metric("⏱️ Minutes per Contribution", "N/A")
    
    # Full stats table
    st.markdown("---")
    with st.expander("📋 **Full Statistics Table**", expanded=False):
        if is_goalkeeper and 'Clean_Sheets' in player_data.index:
            display_cols = ['Player', 'Team', 'Position', 'Appearances', 'Minutes', 'Clean_Sheets', 'Goals_Against']
            if 'Save_Percentage' in player_data.index:
                display_cols.append('Save_Percentage')
        else:
            display_cols = ['Player', 'Team', 'Position', 'Goals', 'Assists', 'Appearances', 'Minutes', 
                            'Goals_per_90', 'Assists_per_90', 'G+A_per_90']
        
        # Only show columns that exist in the dataframe
        available_display_cols = [col for col in display_cols if col in search_filtered_df.columns]
        st.dataframe(search_filtered_df[search_filtered_df["Player"] == player][available_display_cols], use_container_width=True)

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
    
    # Top Goalkeepers
    st.subheader("🧤 Top 10 Goalkeepers")
    goalkeepers_df = df[df['Position'] == 'GK'].copy()
    
    if len(goalkeepers_df) > 0 and 'Clean_Sheets' in goalkeepers_df.columns:
        # Calculate Clean Sheet %
        goalkeepers_df['Clean_Sheet_%'] = (goalkeepers_df['Clean_Sheets'] / goalkeepers_df['Appearances'] * 100).round(1)
        
        # Get top 10 by Clean Sheets
        top_goalkeepers = goalkeepers_df.nlargest(10, 'Clean_Sheets')[['Player', 'Team', 'Appearances', 'Clean_Sheets', 'Goals_Against', 'Clean_Sheet_%', 'Save_Percentage']]
        top_goalkeepers.index = range(1, len(top_goalkeepers) + 1)
        
        # Format Save_Percentage
        top_goalkeepers['Save_Percentage'] = top_goalkeepers['Save_Percentage'].apply(lambda x: f"{x:.1f}%" if x > 0 else "N/A")
        
        st.dataframe(top_goalkeepers, use_container_width=True)
    else:
        st.info("Goalkeeper statistics not available in current dataset.")
    
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
with tab3:
    st.header("👥 Compare Players")
    
    # Add search filters for both players
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Player 1")
        search_term1 = st.text_input("Search Player 1", "", key="search1").strip()
        
        # Filter players based on search term
        if search_term1:
            search_filtered_df1 = filtered_df[filtered_df["Player"].str.contains(search_term1, case=False, na=False)]
        else:
            search_filtered_df1 = filtered_df
        
        player1 = st.selectbox("Select Player 1", search_filtered_df1["Player"].unique(), key="p1")
        player1_data = filtered_df[filtered_df["Player"] == player1].iloc[0]
        
        st.markdown(f"**Position:** {player1_data['Position']}")
        st.markdown(f"**Team:** {player1_data['Team']}")
        st.metric("Goals", int(player1_data["Goals"]))
        st.metric("Assists", int(player1_data["Assists"]))
        st.metric("Appearances", int(player1_data["Appearances"]))
        st.metric("Minutes", int(player1_data["Minutes"]))
    
    with col2:
        st.subheader("Player 2")
        search_term2 = st.text_input("Search Player 2", "", key="search2").strip()
        
        # Filter players based on search term
        if search_term2:
            search_filtered_df2 = filtered_df[filtered_df["Player"].str.contains(search_term2, case=False, na=False)]
        else:
            search_filtered_df2 = filtered_df
        
        player2 = st.selectbox("Select Player 2", search_filtered_df2["Player"].unique(), key="p2")
        player2_data = filtered_df[filtered_df["Player"] == player2].iloc[0]
        
        st.markdown(f"**Position:** {player2_data['Position']}")
        st.markdown(f"**Team:** {player2_data['Team']}")
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
