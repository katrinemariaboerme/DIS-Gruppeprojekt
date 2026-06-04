import sqlite3

""" Establishes a connection to the SQLite database and returns the connection object """
def db_connection():
    conn = sqlite3.connect("watchflix.db")
    conn.row_factory = sqlite3.Row # Makes columns accessible only by name instead of (index, name)
    return conn

""" Initializes the databse by calling db_connection()"""
def init_db():
    conn = db_connection()
    
    # User table, if we want to implelemnt user accounts but let's first focus on the content + credits
    conn.execute("""CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            USERNAME TEXT NOT NULL UNIQUE, 
            password TEXT NOT NULL)""")
    
    # Content, either movie or TV Show
    conn.execute("""CREATE TABLE IF NOT EXISTS Content (
            content_id TEXT PRIMARY KEY, 
            title TEXT NOT NULL,
            show_type TEXT NOT NULL,
            description TEXT,
            release_year INTEGER,
            age_certification TEXT,
            runtime INTEGER,
            genres TEXT,
            production_countries TEXT,
            seasons INTEGER,
            imdb_id TEXT UNIQUE,
            imdb_score REAL,
            imdb_votes INTEGER,
            tmdb_popularity REAL,
            tmdb_score REAL)""")
    
    # Credits, either an actor or director of the content
    conn.execute("""CREATE TABLE IF NOT EXISTS Credits (
            content_id PRIMARY KEY TEXT NOT NULL,
            person_id INTEGER,
            FOREIGN KEY (content_id) REFERENCES Content(content_id),
            name TEXT NOT NULL,
            character_name TEXT,
            role TEXT)""")
    
    # User content lists is the watchlist or the favourites
    conn.execute("""CREATE TABLE IF NOT EXISTS UserContentList (
            user_id INTEGER NOT NULL,
            content_id TEXT NOT NULL,
            status TEXT NOT NULL,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, content_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (content_id) REFERENCES Content(content_id))""")
    
    conn.commit()
    conn.close()
        