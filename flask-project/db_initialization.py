from database import db_connection
import csv, re

""" Initializes the databse by calling db_connection()"""
def init_db():
    conn = db_connection()
    c = conn.cursor()

    # we drop the tables if they already exist
    c.execute("DROP TABLE IF EXISTS Watchlist;")
    c.execute("DROP TABLE IF EXISTS Favourites;")
    c.execute("DROP TABLE IF EXISTS Credits;")
    c.execute("DROP TABLE IF EXISTS Content;")
    
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
            imdb_votes REAL,
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

"""Checks if a Content or Credits entity has a valid content_id (primary key)"""
def check_id(content_id):
    id = str(content_id).strip()
    result = re.fullmatch(r't[ms][0-9]{1,7}$', id) # only content_id's staring with tm or ts followed by 1-7 arbitrary numbers are considered valid
    if result == None:
        return False
    else:
        return True # a match was found so title can be added to our database
    

"""Populates the empty tables with the actual data from the .csv files"""
def fill_db():
    conn = db_connection()
    c = conn.cursor()

    content_path = 'data/titles.csv'
    credits_path = 'data/credits.csv'

    with open(content_path, 'r', encoding='utf-8') as content_file:
        titles = csv.reader(content_file)
        next(titles) # Skipping the column names so we only get the actual data
        
        for content in titles:
            if check_id(content[0]):
                c.execute(""" 
                    INSERT INTO Content 
                    (content_id, title, show_type, description, release_year, age_certification, runtime, genres, production_countries,
                    seasons, imdb_id, imdb_score, imdb_votes, tmdb_popularity, tmdb_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    ON CONFLICT DO NOTHING; """, (
                    content[0], # content_id
                    content[1], # title
                    content[2], # show_type
                    content[3] if content[3] != '' else None, # description
                    content[4] if content[4] != '' else None, # release_year
                    content[5] if content[5] != '' else None, # age_certification
                    content[6] if content[6] != '' else None, # runtime
                    content[7] if content[7] != '' else None, # genres
                    content[8] if content[8] != '' else None, # production_countries
                    content[9] if content[9] != '' else None, # seasons
                    content[10] if content[10] != '' else None, # imdb_id
                    content[11] if content[11] != '' else None, # imdb_score
                    content[12] if content[12] != '' else None, # imdb_votes
                    content[13] if content[13] != '' else None, # tmdb_popularity
                    content[14] if content[14] != '' else None, # tmdb_score
                ))
        conn.commit()
    
    # Same population strategy but now for the actors and directors aka the credits.csv data
    with open(credits_path, 'r', encoding='utf-8') as credits_file:
        credits_read = csv.reader(credits_file)
        next(credits_read) # Skipping the column names so we only get the actual data
        
        for person in credits_read:
            if check_id(person[1]):    
                c.execute(""" 
                    INSERT INTO Credits 
                    (person_id, content_id, name, character_name, role)
                    VALUES (%s, %s, %s, %s, %s) 
                    ON CONFLICT DO NOTHING; """, (
                    person[0], # person_id
                    person[1], # content_id
                    person[2], # name
                    person[3] if person[3] != '' else None, # character
                    person[4] if person[4] != '' else None # role (actor or director)
                ))
        conn.commit()
        conn.close()
        
init_db() 
fill_db()