import psycopg2

""" Connects to the PostgreSQL database and returns the connection object """
def db_connection():
    conn = psycopg2.connect(
        host="database",
        database="watchflix_db", 
        user="postgres",
        password="123" 
    )
    return conn

""" Initializes the databse by calling db_connection()"""
def init_db():
    conn = db_connection()
    c = conn.cursor()

    # we drop the tables if they already exists
    c.execute("DROP TABLE IF EXISTS Watchlist;")
    c.execute("DROP TABLE IF EXISTS Favourites;")
    c.execute("DROP TABLE IF EXISTS Credits;")
    c.execute("DROP TABLE IF EXISTS Content;")

    # I removed 'Users' TABLE, we can always add it if we have more time
    
    # Content, either movie or TV Show
    c.execute("""CREATE TABLE IF NOT EXISTS Content (
            content_id TEXT PRIMARY KEY, 
            title TEXT NOT NULL,
            show_type TEXT NOT NULL,
            description TEXT,
            release_year INTEGER,
            age_certification TEXT,
            runtime INTEGER,
            genres TEXT,
            production_countries TEXT,
            seasons REAL,
            imdb_id TEXT UNIQUE,
            imdb_score REAL,
            imdb_votes INTEGER,
            tmdb_popularity REAL,
            tmdb_score REAL)""")
    
    # Credits, either an actor or director of the content
    c.execute("""CREATE TABLE IF NOT EXISTS Credits (
            id SERIAL PRIMARY KEY,
            person_id INTEGER,
            content_id TEXT NOT NULL,
            name TEXT NOT NULL,
            character_name TEXT,
            role TEXT)""")
    
    # The watchlist, not depending on a user as we wew short on time
    c.execute("""CREATE TABLE IF NOT EXISTS Watchlist (
           content_id TEXT NOT NULL,
           status TEXT NOT NULL,
           added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           PRIMARY KEY (content_id),
           FOREIGN KEY (content_id) REFERENCES Content(content_id))""")
    
    # The favourites list, not depending on a user as we wew short on time
    c.execute("""CREATE TABLE IF NOT EXISTS Favourites (
           content_id TEXT NOT NULL,
           status TEXT NOT NULL,
           added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           PRIMARY KEY (content_id),
           FOREIGN KEY (content_id) REFERENCES Content(content_id))""")
    
    conn.commit()
    c.close()
    conn.close()
        