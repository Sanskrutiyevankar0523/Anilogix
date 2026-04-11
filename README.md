⛩️ AniLogix: Relational Anime Management System
AniLogix is a professional-grade DBMS Project that bridges the gap between raw data and interactive visualization. It utilizes a 3-Tier Architecture to manage anime archives, user authentication, and relational insights through a seamless Python and MySQL integration.

📁 Repository Structure & File Logic
app.py: The core Streamlit application and UI logic.

migrate_to_mysql.py: The data engineering script used to clean and push local data into the MySQL Server.

AniLogix_Permanent.db: A lightweight SQLite version of the database for offline portability.

final_queries.py: A dedicated repository of the complex SQL JOINs used for relational analysis.

requirements.txt: List of all Python dependencies required to run the project.

ER_Diag.png: The Entity-Relationship diagram showing the database schema and constraints.

.csv Files: The raw datasets (Genres, Staff, Characters, etc.) used as the project's foundation.

🚀 Key Features
Sensei (AI Guide): An interactive chatbot using Fuzzy Matching to handle user typos and provide context-aware recommendations.

RBAC Authentication: A secure entry system with a 16+ age gate and math-based human verification (Captcha).

Personalization: Real-time theme customization allowing users to upload backgrounds or enjoy the default Cherry Blossom aesthetic.

Relational Dashboard: Advanced filtering by ratings and titles powered by a live MySQL connection.

🛠️ Tech Stack
Frontend: Streamlit (Python-based Web Framework)

Backend: Python (SQLAlchemy & Pandas)

Database: MySQL Server 8.0 (Permanent Storage)

Fuzzy Logic: thefuzz library for typo-tolerant chat interactions.

🔧 Installation & Setup
1. Database Initialization
Before running the app, ensure your MySQL service is active. You can use the provided migration script to set up your tables:

Bash
python migrate_to_mysql.py
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Launch AniLogix
Bash
streamlit run app.py
🧬 Database Logic & Persistence
Permanent Storage
Unlike session-based storage, AniLogix data is stored in the MySQL Data Directory. The data is managed by the MySQL Daemon, ensuring that all records are ACID-compliant and persist even after the application or system is restarted.

Connectivity Layer
The application uses SQLAlchemy as an abstraction layer to communicate with the MySQL daemon.

Connection Protocol: TCP/IP via mysql-connector-python.

Data Flow: SQL Query → MySQL Server → Pandas DataFrame → Streamlit UI.


Developed by Sanskruti Yevankar
