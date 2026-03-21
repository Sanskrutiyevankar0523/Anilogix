import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import base64
from PIL import Image
import io

# --- 1. DATABASE CONNECTION (MySQL) ---
# Centralized MySQL DB se connection
engine = create_engine('mysql+mysqlconnector://root:sanskruti_23@localhost/Anilogix')

# Page Configuration
st.set_page_config(page_title="AniLogix Dashboard", page_icon="🏮", layout="wide")

# --- 2. CUSTOM LOGO & CSS ---
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Orbitron:wght@700&display=swap');
        .logo-text {
            font-family: 'Orbitron', sans-serif;
            color: #fff;
            font-size: 60px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 5px;
            text-shadow: 0 0 10px #FF4B4B, 0 0 20px #FF4B4B, 0 0 30px #FF4B4B;
            margin-bottom: 20px;
        }
        .anime-card {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            color: white;
            transition: 0.4s;
            height: 200px;
        }
        .anime-card:hover {
            border: 1px solid #FF4B4B;
            box-shadow: 0 0 15px rgba(255, 75, 75, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- 3. DYNAMIC BACKGROUND LOGIC ---
def set_bg(image_file):
    if image_file is not None:
        img = Image.open(image_file)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode()
    else:
        try:
            with open("image_e3f03c.jpg", "rb") as f:
                encoded_img = base64.b64encode(f.read()).decode()
        except:
            encoded_img = ""

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_img}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR: CUSTOMIZATION & FILTERS ---
st.sidebar.markdown("# 🎨 Customization")
custom_bg = st.sidebar.file_uploader("Upload Background Image", type=["jpg", "png", "jpeg"])
set_bg(custom_bg)

st.sidebar.markdown("---")
search_query = st.sidebar.text_input("🔍 Search Anime Title:")
score_min = st.sidebar.slider("⭐ Min Rating", 0.0, 10.0, 7.5)

# --- 5. HEADER LOGO ---
st.markdown('<div class="logo-text">⛩️ AniLogix ⛩️</div>', unsafe_allow_html=True)

# --- 6. MAIN CONTENT & 7-TABLE LOGIC ---
if search_query:
    # SQL JOIN for search
    sql = f"""
        SELECT a.anime_id, a.title, r.score, a.type 
        FROM Anime a 
        JOIN Ratings r ON a.anime_id = r.anime_id 
        WHERE a.title LIKE '%%{search_query}%%' AND r.score >= {score_min} 
        LIMIT 12
    """
    try:
        data = pd.read_sql(sql, con=engine)
        
        if not data.empty:
            cols = st.columns(3)
            for i, row in data.iterrows():
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="anime-card">
                            <h3>{row['title']}</h3>
                            <p>Score: ⭐ {row['score']}</p>
                            <p>Format: {row['type']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            selected_title = st.selectbox("Select Anime for Full Details (Relational View):", data['title'].unique())
            
            if selected_title:
                a_id = data[data['title'] == selected_title]['anime_id'].values[0]
                
                # Characters (Fixed: Using IDs only)
                char_df = pd.read_sql(f"SELECT character_id, role FROM Characters WHERE anime_id = {a_id}", con=engine)
                
                # Voice Actors (Relational Link)
                actor_query = f"""
                    SELECT v.person_id, v.language 
                    FROM Voice_Actors v
                    JOIN Characters c ON v.character_id = c.character_id
                    WHERE c.anime_id = {a_id}
                """
                actor_df = pd.read_sql(actor_query, con=engine)
                
                # Companies (Fixed: Removed 'name' column which caused error)
                # Hum yahan 'company_id' aur 'type' select kar rahe hain
                try:
                    comp_df = pd.read_sql(f"SELECT * FROM Companies WHERE anime_id = {a_id}", con=engine)
                except:
                    comp_df = pd.DataFrame(["No Company Data Found"])

                t1, t2, t3 = st.tabs(["🎭 Characters", "🎙️ Voice Cast", "🏢 Production"])
                with t1: 
                    st.write("Relational Data: Character IDs and Roles")
                    st.table(char_df)
                with t2: 
                    st.write("Voice Actor IDs and Language Details")
                    st.table(actor_df)
                with t3: 
                    st.write("Production House Information (Relational IDs)")
                    st.table(comp_df)
        else:
            st.error("No results found.")
    except Exception as e:
        st.error(f"MySQL Error: {e}")

else:
    st.info("Sidebar se search karein!")
    top_sql = """
        SELECT a.title, r.score, a.type 
        FROM Anime a 
        JOIN Ratings r ON a.anime_id = r.anime_id 
        ORDER BY r.score DESC LIMIT 6
    """
    top_data = pd.read_sql(top_sql, con=engine)
    st.write("### 🔥 Current Top Rated (MySQL Centralized)")
    st.table(top_data)