import pandas as pd
from sqlalchemy import create_engine, text

# MySQL Connection
db_url = 'mysql+mysqlconnector://root:sanskruti_23@localhost/Anilogix'
engine = create_engine(db_url)

try:
    print("⏳ Adding new tables to AniLogix Centralized DB...")
    
    # Load all CSVs (Purani + Nayi)
    anime_df = pd.read_csv('anime.csv')
    staff_df = pd.read_csv('anime_staff.csv')
    genres_df = pd.read_csv('anime_genres.csv')
    
    # Nayi CSV Files
    actors_df = pd.read_csv('anime_voice_actors.csv')
    companies_df = pd.read_csv('anime_companies.csv')
    chars_df = pd.read_csv('anime_characters.csv')

    with engine.connect() as conn:
        # Purani tables drop karke fresh start karenge taaki consistency rahe
        conn.execute(text("DROP TABLE IF EXISTS Staff, Genres, Ratings, Voice_Actors, Companies, Characters, Anime"))
        
        # 1. Base Table: Anime
        anime_df[['anime_id', 'title', 'type']].to_sql('Anime', con=conn, if_exists='replace', index=False)
        
        # 2. Existing Relations
        staff_df.to_sql('Staff', con=conn, if_exists='replace', index=False)
        genres_df.to_sql('Genres', con=conn, if_exists='replace', index=False)
        anime_df[['anime_id', 'score']].to_sql('Ratings', con=conn, if_exists='replace', index=False)
        
        # 3. New Relations (Errorless Addition)
        print("📦 Pushing Voice Actors...")
        actors_df.to_sql('Voice_Actors', con=conn, if_exists='replace', index=False)
        
        print("📦 Pushing Companies...")
        companies_df.to_sql('Companies', con=conn, if_exists='replace', index=False)
        
        print("📦 Pushing Characters...")
        chars_df.to_sql('Characters', con=conn, if_exists='replace', index=False)
        
        conn.commit()

    print("\n🎉 Success! All 7 tables are now LIVE in MySQL.")

except Exception as e:
    print(f"\n❌ Error: {e}")