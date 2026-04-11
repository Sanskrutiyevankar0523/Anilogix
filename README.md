# 🏮 AniLogix: Relational Anime Management System

AniLogix is a full-stack **DBMS Project** that combines the power of **MySQL** with an interactive **Streamlit** dashboard. It features an AI-inspired "Sensei" chatbot, dynamic theme personalization, and advanced relational queries.

## 🚀 Features
* **Sensei Chatbot**: An interactive guide using fuzzy matching to suggest anime and recall context.
* **Authentication**: 16+ Age Gate and Human-Verification (Captcha) for secure entry.
* **Dynamic Styling**: Cherry blossom animations and user-driven theme uploads.
* **Relational Insights**: Real-time filtering across Anime, Ratings, and Genre tables.

## 🛠️ Tech Stack
* **Frontend**: Streamlit (Python)
* **Backend**: Python (SQLAlchemy)
* **Database**: MySQL Workbench
* **Fuzzy Logic**: TheFuzz (Levenshtein Distance)

## 🔧 Installation & Setup
1. **Clone the repo**:
   ```bash
  [ git clone [https://github.com/YourUsername/AniLogix-DBMS.git](https://github.com/YourUsername/AniLogix-DBMS.git)](https://github.com/Sanskrutiyevankar0523/AniLogix.git)
   
 ### Step 2: Install Dependencies
` ``bash
pip install -r requirements.txt
` ``

### Step 3: Database Configuration
1. Open **MySQL Workbench**.
2.Run the migrate_to_mysql.py script to clean and push the CSV data to your local MySQL server.
3. Update the `engine` connection string in `app.py` with your MySQL password.

### Step 4: Run the Application
` ``bash
streamlit run app.py
` ``

---

## 🗄️ Database Logic & Connectivity
AniLogix uses a **3-Tier Architecture** to ensure data is never lost:
1. **Presentation Layer**: Streamlit UI for user interaction.
2. **Application Layer**: Python (SQLAlchemy) handling the business logic and fuzzy matching.
3. **Database Layer**: MySQL Server providing permanent, ACID-compliant storage.

**How it stays permanent:** Even when you turn off your computer, the data is saved in MySQL's physical storage files. The **MySQL Daemon** manages these files, ensuring that your anime list and user accounts are always there when you restart the app.

## 🧬 Technical Deep Dive

### 🔌 How Python & SQL Connect
The connection is established using **SQLAlchemy** acting as an abstraction layer over the `mysql-connector-python` driver. 
1. **The Engine**: `create_engine()` initializes a pool of connections to the local MySQL server.
2. **Vectorized Retrieval**: We use `pd.read_sql()`, which executes raw SQL strings and immediately converts the result sets into Pandas DataFrames for high-speed UI rendering.

### 💾 Permanent Storage Logic
Unlike temporary arrays or local dictionaries, AniLogix data is stored in the **MySQL Data Directory**. 
* **Persistence**: When a user adds an anime or creates an account, it is committed to the disk. 
* **Service-Based**: The data is managed by the MySQL Service (Daemon), meaning the database remains accessible to any client (Python, Workbench, or Command Line) as long as the service is running.

### Project Screenshots

<img width="1911" height="969" alt="Screenshot 2026-04-12 001834" src="https://github.com/user-attachments/assets/633d1f21-a35d-482f-ad02-28e29b9cbe5f" />
<img width="1917" height="978" alt="Screenshot 2026-04-12 001641" src="https://github.com/user-attachments/assets/43e7cfb3-ca0d-4429-b342-31e9b1ecdb6e" />
<img width="1905" height="976" alt="Screenshot 2026-04-12 001320" src="https://github.com/user-attachments/assets/c6a80139-372c-4004-a9b7-bfec23cb416a" />

