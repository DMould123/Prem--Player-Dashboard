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
    
    # Map to our required format (adjust column names based on what's available)
    # You may need to adjust these column names based on the actual CSV
    if 'Player' in df.columns and 'Squad' in df.columns:
        df_clean = df[['Player', 'Squad', 'Gls', 'Ast', 'MP', 'Min']].copy()
        df_clean.columns = ['Player', 'Team', 'Goals', 'Assists', 'Appearances', 'Minutes']
        
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