import kagglehub
import pandas as pd
import os
import shutil
import requests
from io import StringIO

# Download general player stats from Kaggle
path = kagglehub.dataset_download("siddhrajthakor/fbref-premier-league-202425-player-stats-dataset")

print("Path to dataset files:", path)

# Find the CSV file in the downloaded path
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

if csv_files:
    # Use the first CSV file found
    source_file = os.path.join(path, csv_files[0])
    
    # Read and process the data
    df = pd.read_csv(source_file)
    
    # Check what columns are available
    print("Available columns:", df.columns.tolist())
    
    # Map to our required format INCLUDING position
    if 'Player' in df.columns and 'Squad' in df.columns:
        # Basic columns for all players
        base_cols = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', 'Gls', 'Ast', 'MP', 'Min']
        
        # Check for goalkeeper-specific columns (if they exist)
        gk_cols = []
        if 'CS' in df.columns:  # Clean Sheets
            gk_cols.append('CS')
        if 'GA' in df.columns:  # Goals Against
            gk_cols.append('GA')
        if 'Save%' in df.columns or 'Saves%' in df.columns:  # Save Percentage
            gk_cols.append('Save%' if 'Save%' in df.columns else 'Saves%')
        
        # Combine columns
        all_cols = base_cols + gk_cols
        available_cols = [col for col in all_cols if col in df.columns]
        
        df_clean = df[available_cols].copy()
        
        # Rename basic columns
        rename_map = {
            'Player': 'Player',
            'Nation': 'Nationality', 
            'Pos': 'Position',
            'Squad': 'Team',
            'Age': 'Age',
            'Born': 'Year_Born',
            'Gls': 'Goals',
            'Ast': 'Assists',
            'MP': 'Appearances',
            'Min': 'Minutes'
        }
        
        # Add GK stat renames if they exist
        if 'CS' in df_clean.columns:
            rename_map['CS'] = 'Clean_Sheets'
        if 'GA' in df_clean.columns:
            rename_map['GA'] = 'Goals_Against'
        if 'Save%' in df_clean.columns:
            rename_map['Save%'] = 'Save_Percentage'
        if 'Saves%' in df_clean.columns:
            rename_map['Saves%'] = 'Save_Percentage'
        
        df_clean = df_clean.rename(columns=rename_map)
        
        # Standardize positions - handle multiple separators and classify properly
        def standardize_position(pos):
            if pd.isna(pos):
                return 'Unknown'
            
            # Convert to string and clean
            pos_str = str(pos).strip()
            
            # Split by comma or space to get primary position
            for sep in [',', ' ']:
                if sep in pos_str:
                    pos_str = pos_str.split(sep)[0].strip()
                    break
            
            # Categorize versatile players
            # FW,MF or MF,FW (wingers, attacking mids) -> classify as their primary position
            pos_upper = pos_str.upper()
            
            # Standard positions
            if pos_upper in ['GK', 'DF', 'MF', 'FW']:
                return pos_upper
            
            # If it's still combined after split, take first 2 characters
            if len(pos_upper) > 2:
                return pos_upper[:2]
            
            return pos_upper
        
        df_clean['Position'] = df_clean['Position'].apply(standardize_position)
        
        # Clean nationality - extract just the 3-letter country code
        def clean_nationality(nat):
            if pd.isna(nat):
                return 'Unknown'
            # Nationality format is like "eng ENG" or "ch SUI" - take the last 3 characters
            nat_str = str(nat).strip()
            # Split by space and take the last part (the uppercase code)
            parts = nat_str.split()
            if len(parts) > 1:
                return parts[-1]  # Return the last part (e.g., "ENG", "SUI", "USA")
            return nat_str.upper()
        
        df_clean['Nationality'] = df_clean['Nationality'].apply(clean_nationality)
        
        # Scrape goalkeeper stats from FBref
        print("\nFetching goalkeeper statistics from FBref...")
        try:
            import time
            gk_url = "https://fbref.com/en/comps/9/keepers/Premier-League-Stats"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
            
            # Add delay to be respectful
            time.sleep(3)
            
            response = requests.get(gk_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse goalkeeper stats table
            gk_tables = pd.read_html(StringIO(response.text))
            
            # The goalkeeper stats table is usually the first one
            gk_df = gk_tables[0]
            
            # Handle multi-level columns if they exist
            if isinstance(gk_df.columns, pd.MultiIndex):
                gk_df.columns = ['_'.join(col).strip() if col[1] else col[0] for col in gk_df.columns.values]
            
            # Find relevant GK columns (adjust based on actual table structure)
            # Common columns: Player, CS (Clean Sheets), GA (Goals Against), Save% or SoT% (Save Percentage)
            gk_cols_map = {}
            for col in gk_df.columns:
                col_lower = str(col).lower()
                if 'player' in col_lower and 'Player' not in gk_cols_map:
                    gk_cols_map['Player'] = col
                elif 'cs' in col_lower or 'clean' in col_lower:
                    gk_cols_map['Clean_Sheets'] = col
                elif 'ga' in col_lower and 'goal' in col_lower and 'against' in col_lower:
                    gk_cols_map['Goals_Against'] = col
                elif 'save%' in col_lower or 'sv%' in col_lower:
                    gk_cols_map['Save_Percentage'] = col
            
            if 'Player' in gk_cols_map and len(gk_cols_map) > 1:
                # Extract GK stats
                gk_stats = gk_df[[gk_cols_map[k] for k in gk_cols_map.keys() if k in gk_cols_map]].copy()
                gk_stats.columns = list(gk_cols_map.keys())
                
                # Clean player names (remove any extra characters)
                gk_stats['Player'] = gk_stats['Player'].str.strip()
                
                # Convert numeric columns
                for col in ['Clean_Sheets', 'Goals_Against', 'Save_Percentage']:
                    if col in gk_stats.columns:
                        gk_stats[col] = pd.to_numeric(gk_stats[col], errors='coerce')
                
                # Merge with main dataframe
                df_clean = df_clean.merge(gk_stats, on='Player', how='left')
                print(f"✓ Added goalkeeper stats for {gk_stats['Player'].nunique()} goalkeepers")
            else:
                print("⚠️ Could not find goalkeeper stats columns in expected format")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("⚠️ FBref is blocking automated requests. Goalkeeper stats unavailable.")
                print("   Alternative: Manually download goalkeeper data from FBref and add to CSV")
            else:
                print(f"⚠️ HTTP Error {e.response.status_code}: {str(e)}")
            print("Continuing with player stats only...")
        except Exception as e:
            print(f"⚠️ Could not fetch goalkeeper stats: {str(e)}")
            print("Continuing with player stats only...")
        
        # Save to your project directory
        df_clean.to_csv('premier_league_stats.csv', index=False)
        print(f"✓ Fetched {len(df_clean)} players!")
        print(f"✓ Saved to premier_league_stats.csv")
    else:
        # If column names don't match, just copy the file
        shutil.copy(source_file, 'premier_league_stats.csv')
        print(f"✓ Downloaded and saved dataset")
else:
    print("No CSV files found in the dataset")