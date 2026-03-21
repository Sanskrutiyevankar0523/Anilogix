import sqlite3
import pandas as pd

conn = sqlite3.connect('AniLogix_Permanent.db')
# Anime table ki pehli 20 rows dikhane ke liye
df = pd.read_sql_query("SELECT * FROM Anime LIMIT 20", conn)
print(df)
conn.close()