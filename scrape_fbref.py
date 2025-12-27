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
        df_clean = df[['Player', 'Squad', 'Pos', 'Gls', 'Ast', 'MP', 'Min']].copy()
        df_clean.columns = ['Player', 'Team', 'Position', 'Goals', 'Assists', 'Appearances', 'Minutes']
        
        # Standardize positions - take only the primary position (first one)
        def standardize_position(pos):
            if pd.isna(pos):
                return 'Unknown'
            # Take only the first position if multiple are listed
            primary_pos = str(pos).split(',')[0].strip()
            return primary_pos
        
        df_clean['Position'] = df_clean['Position'].apply(standardize_position)
        
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