import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import base64
from PIL import Image
import io
import random
from thefuzz import process

# --- 1. DATABASE CONNECTION ---
engine = create_engine('mysql+mysqlconnector://root:sanskruti_23@localhost/Anilogix')

# Page Configuration
st.set_page_config(page_title="AniLogix Pro", page_icon="🏮", layout="wide")

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'captcha_n1' not in st.session_state:
    st.session_state.captcha_n1 = random.randint(1, 10)
    st.session_state.captcha_n2 = random.randint(1, 10)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. CUSTOM CSS ---
def local_css():
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Orbitron:wght@700&display=swap');
        
        .block-container {{ padding-top: 0rem !important; }}
        [data-testid="stHeader"] {{ background: rgba(0,0,0,0) !important; }}

        label {{
            color: black !important;
            font-weight: bold !important;
            font-size: 20px !important;
            text-shadow: 2px 2px 8px white !important;
        }}

        .logo-text {{
            font-family: 'Orbitron', sans-serif;
            color: #FF4B4B;
            font-size: 60px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 5px;
            text-shadow: 3px 3px 10px rgba(0,0,0,0.7);
            margin-top: 30px;
        }}

        div.stButton > button {{
            background: linear-gradient(90deg, #FF4B4B, #f093fb);
            color: white;
            font-size: 18px !important;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }}

        @keyframes petal-fall {{
            0% {{ transform: translateY(-10%) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
        }}
        .petal {{
            position: fixed;
            background-color: #ffb7c5;
            border-radius: 150% 0 150% 0;
            width: 12px;
            height: 8px;
            z-index: 999;
            pointer-events: none;
            animation: petal-fall 10s linear infinite;
        }}

        [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {{
            color: black !important;
            font-weight: bold !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 4. BACKGROUND LOGIC ---
def set_bg(image_file, is_login=False):
    if is_login:
        bg_url = "https://wallpapercave.com/wp/wp6658145.jpg" 
    elif image_file is not None:
        img = Image.open(image_file)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        bg_url = f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
    else:
        bg_url = "https://img.freepik.com/free-vector/white-abstract-background-design_23-2148825582.jpg"

    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-position: center top;
        }}
        </style>
        {"".join([f'<div class="petal" style="left:{random.randint(5,95)}%; animation-delay:{random.randint(0,5)}s;"></div>' for _ in range(8)])}
    """, unsafe_allow_html=True)

# --- 5. THE SENSEI CHAT BOT ---
def sensie_bot():
    st.markdown("### ⛩️ Sensei: Your Anime Guide")
    
    # Initialize history and memory
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_suggested_id" not in st.session_state:
        st.session_state.last_suggested_id = None

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🏮" if message["role"] == "assistant" else None):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Sensei something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = ""
        low_prompt = prompt.lower()
        
        # --- 1. HANDLING TYPOS (Fuzzy Matching) ---
        genres = ['comedy', 'action', 'romance', 'drama', 'horror', 'sci-fi', 'adventure', 'thriller']
        # Extract keywords and find the closest match
        words = low_prompt.split()
        match, score = process.extractOne(low_prompt, genres) if words else (None, 0)
        
        # --- 2. CONTEXTUAL MEMORY (Handling "that" or "rating") ---
        if ("rating" in low_prompt or "score" in low_prompt) and st.session_state.last_suggested_id:
            rating_sql = f"SELECT score FROM Ratings WHERE anime_id = {st.session_state.last_suggested_id}"
            res = pd.read_sql(rating_sql, con=engine)
            response = f"The scrolls show a rating of ⭐ **{res['score'][0]}** for that masterpiece." if not res.empty else "I cannot find the rating right now."

        # --- 3. GENRE SEARCH (If not a follow-up) ---
        elif score > 70: # If match is likely a typo of a genre
            bot_sql = f"""
                SELECT a.anime_id, a.title FROM Anime a
                JOIN Genres g ON a.anime_id = g.anime_id
                JOIN Ratings r ON a.anime_id = r.anime_id
                WHERE g.genre LIKE '%%{match}%%' AND r.score > 8.0
                ORDER BY RAND() LIMIT 1
            """
            res = pd.read_sql(bot_sql, con=engine)
            if not res.empty:
                st.session_state.last_suggested_id = res['anime_id'][0] # Store ID for next question
                response = f"Ah, {match}! Sensei suggests: **{res['title'][0]}**. A fine choice for your soul."
            else:
                response = f"I found no {match} scrolls today. Try another genre!"
        
        else:
            response = "I am listening. Mention a genre like 'Action' or ask about the 'rating' of my last suggestion!"

        with st.chat_message("assistant", avatar="🏮"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# --- 6. AUTHENTICATION ---
def auth_page():
    local_css()
    st.markdown('<div class="logo-text">⛩️ AniLogix ⛩️</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "📝 SIGN UP"])
        with tab1:
            st.text_input("Email", key="log_email")
            st.text_input("Password", type="password", key="log_pass")
            if st.button("LOG IN"):
                st.session_state['logged_in'] = True
                st.rerun()
        with tab2:
            st.text_input("Full Name", key="reg_name")
            st.number_input("Age", min_value=1, value=18)
            n1, n2 = st.session_state.captcha_n1, st.session_state.captcha_n2
            captcha = st.number_input(f"Check: {n1} + {n2}", step=1)
            if st.button("CREATE ACCOUNT"):
                if captcha == (n1 + n2): st.success("Account Created!")

# --- 7. MAIN DASHBOARD ---
def main_dashboard():
    local_css()
    
    st.sidebar.markdown("### 🎨 CUSTOMIZE")
    custom_bg = st.sidebar.file_uploader("Change Theme", type=["jpg", "png"])
    set_bg(custom_bg, is_login=False)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 SEARCH & FILTER")
    search_query = st.sidebar.text_input("Search Anime Title:")
    score_min = st.sidebar.slider("⭐ Minimum Rating Bar", 0.0, 10.0, 7.5)
    
    # SENSEI BOT INTEGRATION
    st.sidebar.markdown("---")
    with st.sidebar.expander("💬 Summon Sensei"):
        sensie_bot()
    
    if st.sidebar.button("LOGOUT"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.markdown('<div class="logo-text">⛩️ AniLogix ⛩️</div>', unsafe_allow_html=True)
    
    sql = f"""
        SELECT a.title, r.score, a.type 
        FROM Anime a 
        JOIN Ratings r ON a.anime_id = r.anime_id 
        WHERE a.title LIKE '%%{search_query}%%' AND r.score >= {score_min}
        ORDER BY r.score DESC LIMIT 10
    """
    try:
        data = pd.read_sql(sql, con=engine)
        st.dataframe(data.style.set_properties(**{'color': 'black', 'font-weight': 'bold', 'background-color': 'rgba(255,255,255,0.7)'}))
    except Exception as e:
        st.error(f"Error: {e}")

# --- 8. FLOW ---
if not st.session_state['logged_in']:
    set_bg(None, is_login=True)
    auth_page()
else:
    main_dashboard()
    main_dashboard()
