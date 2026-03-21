import os
import pandas as pd
import sqlite3

conn = sqlite3.connect('AniLogix_Permanent.db')

try:
    # 1. Main Anime Table
    anime = pd.read_csv('anime.csv')
    anime.to_sql('Anime', conn, if_exists='replace', index=False)
    
    # 2. Staff Table (Director/Writer ke liye)
    if 'anime_staff.csv' in os.listdir():
        staff = pd.read_csv('anime_staff.csv')
        staff.to_sql('Staff', conn, if_exists='replace', index=False)
        
    # 3. Genres Table
    if 'anime_genres.csv' in os.listdir():
        genres = pd.read_csv('anime_genres.csv')
        genres.to_sql('Genres', conn, if_exists='replace', index=False)

    print("Mubarak ho! Database with Staff & Genres ready hai.")
except Exception as e:
    print(f"Error: {e}")

conn.close()