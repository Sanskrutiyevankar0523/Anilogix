import sqlite3
import pandas as pd

# Database se connect karo
conn = sqlite3.connect('AniLogix_Permanent.db')

print("\n--- TEST: DATA PRESENT HAI YA NAHI? ---")
# Check karte hain ki Anime table mein kitne rows hain
res = pd.read_sql_query("SELECT COUNT(*) as Total_Anime FROM Anime", conn)
print(res)

print("\n--- TOP 5 ANIME BY SCORE ---")
q1 = "SELECT title, score, type FROM Anime WHERE score > 0 ORDER BY score DESC LIMIT 5;"
print(pd.read_sql_query(q1, conn))

conn.close()