import kagglehub
import pandas as pd
import os
import shutil

# Download latest version
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
        df_clean = df[['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', 'Gls', 'Ast', 'MP', 'Min']].copy()
        df_clean.columns = ['Player', 'Nationality', 'Position', 'Team', 'Age', 'Year_Born', 'Goals', 'Assists', 'Appearances', 'Minutes']
        
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