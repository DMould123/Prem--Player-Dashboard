Premier League Player Dashboard ⚽

A web-based interactive dashboard built with Streamlit to visualize Premier League player statistics for the 2024–25 season.

📋 Table of Contents

Features

Prerequisites

Installation

Usage

Project Structure

Data Source

Available Statistics

Updating Data

Troubleshooting

Contributing

License

Support

✨ Features

📊 View comprehensive statistics for 574+ Premier League players

🔍 Interactive player selection via dropdown

⚽ Filter players by team and position (GK, DF, MF, FW)

🏆 Leaderboards showing top 10 goal scorers, assist providers, and total contributors

📈 Visual charts for Goals vs Assists

👥 Side-by-side player comparison mode

📉 Per-game statistics (goals/assists per game)

📑 Organized tab interface (Player Stats, Leaderboards, Compare Players)

🔄 Real-time data from FBref via Kaggle API

💻 Clean and intuitive web interface

⚡ Fast data loading and visualization

🔧 Prerequisites

Before you begin, make sure you have the following installed:

Python 3.8 or higher

pip (Python package installer)

Internet connection (for downloading player data)

Check Python installation
python --version


If Python is not installed, download it from python.org

Make sure to check “Add Python to PATH” during installation.

📦 Installation
1. Clone or download the repository
git clone https://github.com/yourusername/Prem--Player-Dashboard.git
cd Prem--Player-Dashboard


Or download and extract the ZIP file.

2. Install required Python packages
python -m pip install streamlit pandas matplotlib kagglehub


Packages used:

streamlit – Web application framework

pandas – Data manipulation and analysis

matplotlib – Data visualization

kagglehub – Kaggle dataset downloader

🚀 Usage
Step 1: Download the latest player data

Run the scraper script to fetch current Premier League statistics.

Expected result:
Creates or updates premier_league_stats.csv with real 2024–25 season data.

Step 2: Launch the dashboard
streamlit run app.py


Expected result:
The dashboard opens automatically in your default web browser.

Step 3: Explore the dashboard

The dashboard has 3 main tabs:

🏠 **Player Stats** - View individual player statistics and charts

🏆 **Leaderboards** - See top 10 performers (goals, assists, total contributions)

👥 **Compare Players** - Side-by-side comparison of two players

Use the sidebar to filter by team and/or position across all tabs

📁 Project Structure
File	Description
app.py	Streamlit web application
scrape_fbref.py	Script to download and process player data
premier_league_stats.csv	Player statistics (generated after scraping)
README.md	Project documentation
📊 Data Source

Player statistics are sourced from FBref via Kaggle.

Dataset: FBref Premier League 2024–25 Player Stats

Provider: FBref (Football Reference)

Season: 2024–25 Premier League

Update Method: Kaggle API

Total Players: 574+

📈 Available Statistics
Statistic	Description
Player	Full player name
Position	Player position (GK, DF, MF, FW)
Team	Current club
Goals	Total goals scored
Assists	Total assists
Appearances	Matches played (MP)
Minutes	Minutes played
🔄 Updating Data

To refresh the dashboard with the latest statistics:

Re-run the scraper
This overwrites premier_league_stats.csv with updated data.

Refresh the dashboard

If running: refresh the browser (F5)

If stopped: restart with streamlit run app.py

💡 Tip: Run the scraper weekly to keep stats up to date.

🛠️ Troubleshooting
Issue: Module not found

Solution:
Ensure all dependencies are installed using pip.

Issue: Dashboard won’t start

Solution:
Check for syntax errors and confirm Streamlit is installed.

Issue: No data showing

Cause:
premier_league_stats.csv is missing or empty.

Solution:
Re-run the scraper script.

Issue: Kaggle download fails

Possible causes:

No internet connection

Kaggle API rate limit

Dataset renamed or removed

Solution:

Check internet connection

Wait and retry

Verify dataset exists on Kaggle

🤝 Contributing

Contributions are welcome!

How to contribute:

Fork the repository

Create a new branch

git checkout -b feature/improvement


Commit your changes

git commit -am "Add new feature"


Push the branch

git push origin feature/improvement


Open a Pull Request

Ideas for contributions:

Add advanced stats (xG, passes, tackles)

Team-based filtering

Player comparison feature

Advanced visualizations

Export functionality (PDF / Excel)

Search functionality

📝 License

This project is for educational purposes only.

Data attribution:
Player statistics © FBref.com
Dataset provided via Kaggle user siddhrajthakor

Disclaimer:
This project is not affiliated with or endorsed by the Premier League, FBref, or Kaggle.

📞 Support

If you have questions or issues:

Check the Troubleshooting section

Review Usage instructions

Open an issue on GitHub

🎯 Quick Start

python scrape_fbref.py
streamlit run app.py


❤️ Made with love for Premier League fans