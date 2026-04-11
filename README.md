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

### Prerequisites
* **Python 3.10+**
* **MySQL Server** & MySQL Workbench
* **Git** installed on your system

### Step 1: Clone the Repository
```bash
git clone [https://github.com/YourUsername/AniLogix.git](https://github.com/YourUsername/AniLogix.git)
cd AniLogix
  ```
### Step 2: Install Dependencies
` ``bash
pip install -r requirements.txt
` ``

### Step 3: Database Configuration
1. Open **MySQL Workbench**.
2. Execute the `schema.sql` script to build the relational structure.
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
