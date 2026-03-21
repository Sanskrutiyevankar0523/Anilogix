# AniLogix: Anime Management System

AniLogix is a relational database project designed to manage and analyze extensive anime datasets. It provides a user-friendly interface to explore anime details, ratings, characters, and production staff.

## 🚀 Project Overview
The system is built on a **Star-Schema** inspired relational model with 7 interconnected tables. It handles data migration from raw CSV files into a structured SQL environment, ensuring data integrity and optimized querying.

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Python)
- **Database**: MySQL / SQLite
- **Data Handling**: Pandas & SQL Connector
- **Theory**: Relational Algebra & Tuple Relational Calculus

## 📊 Database Schema
The database consists of the following entities:
- **Anime**: The master table containing core titles and types.
- **Ratings**: Performance metrics for each title.
- **Genres**: Categorical classification.
- **Characters & Voice Actors**: A 1:N relationship mapping characters to their multilingual voice cast.
- **Staff & Companies**: Details regarding production roles and studios.

## ⚙️ How to Run

### 1. Database Initialization & Migration
First, set up the database structure and migrate the CSV data:
```bash
python create_db.py
python migrate_to_mysql.py