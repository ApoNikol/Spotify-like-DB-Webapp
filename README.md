# Spotify-like-DB-Webapp
This project is a comprehensive database management system designed to simulate the core functionalities of Spotify. It features a robust relational database integrated with a web-based interface for managing musical content, users, and playlists.
# Spotify-like Database Management System

A full-stack database application designed to simulate the core structure and functionality of a music streaming service like Spotify. This project demonstrates the end-to-end process of database design (ERD, Relational Schema), normalization (3NF), and implementation using PostgreSQL and Python (Flask).

## 📖 Project Overview

The goal of this project was to design a robust database architecture capable of handling users, songs, albums, playlists, and podcasts, and to build a web interface for interacting with this data.

Instead of using pre-packaged tools like Microsoft Access, this project implements a dynamic system using **Python** and **PostgreSQL**. It focuses on data integrity, efficient SQL queries, and a custom-built web frontend.

### Key Features
* **Data Management:** Insert songs, albums, podcasts, and playlists directly into the database.
* **Search Functionality:** Dynamic search with filters to retrieve songs, playlists, and artist data.
* **Data Integrity:** Implementation of constraints (Primary/Foreign Keys) and normalization up to **3rd Normal Form (3NF)** to ensure atomic values and eliminate redundancy.
* **Smart Logic:**
    * **Automatic Artist Creation:** If a song is added with a new artist, the system automatically creates the artist entry in the user table.
    * **Cascading Deletes:** Deleting a playlist removes associated song links; deleting a song removes it from all playlists first to maintain consistency.

## 🛠️ Tech Stack

* **Database:** PostgreSQL
* **Backend:** Python 3.x, Flask Framework, `psycopg2` library
* **Frontend:** HTML5, CSS3, JavaScript
* **Design Tools:** ERD Tools for database modeling

## 📂 Project Structure

```text
├── backend/
│   ├── app.py              # Main Flask application and DB connection logic
│   └── requirements.txt    # Python dependencies
├── database/
│   ├── spotify.sql         # SQL script for schema creation
│   ├── spotify.erd.erdt    # Entity-Relationship Diagram source
│   ├── SXESIAKO-SXHMA.pdf  # Relational Schema Documentation
│   └── FUNCTIONAL-DEPENDENCIES.pdf
└── frontend/
    ├── index.html          # Main dashboard (Switchboard simulation)
    ├── add_song.html       # Data insertion forms
    ├── add_playlist.html   # Playlist management
    ├── css/                # Stylesheets
    └── js/                 # Client-side logic
```
## 💾 Database Design
The database was rigorously designed before implementation:

ER Diagram: Modeled entities (User, Song, Album, Podcast, Playlist) and relationships.

Relational Schema: Converted the ERD into a relational schema, embedding foreign keys to handle 1:N relationships and creating junction tables (e.g., songlist) for M:N relationships.

Normalization: The schema was normalized to BCNF/3NF. We ensured all attributes depend directly on the primary key and eliminated multi-valued attributes (e.g., creating a separate FEATURES table).

## 🚀 Installation & Setup
Follow these steps to run the project locally.

1. Prerequisites
Python 3.x installed.

PostgreSQL installed and running.

2. Database Setup
Open your PostgreSQL client (e.g., pgAdmin or terminal).

Create a new database named spotify database.

Execute the database/spotify.sql script to create the tables and relationships.

3. Application Setup
Clone this repository.

Navigate to the project folder and install the required libraries:

Bash

pip install -r backend/requirements.txt

(Requires flask and psycopg2) .

4. Configure Connection
Open backend/app.py and update the create_connection function with your PostgreSQL credentials :

Python

def create_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="spotify database",
        user="postgres",        # Change to your postgres username
        password="your_password" # Change to your postgres password
    )
5. Run the App
Navigate to the backend directory and run:

Bash

python app.py
Open your browser and go to http://127.0.0.1:5000/ (or open frontend/index.html directly if configured for static serving).
