from database import db_connection


def get_content_homepage():
    conn = db_connection()
    c = conn.cursor()

    content = c.execute("""
        SELECT content_id, title, show_type, release_year, imdb_score
        FROM Content
        ORDER BY imdb_score DESC NULLS LAST
        LIMIT 500;
    """)

    content = c.fetchall()
    conn.close()
    return content


def search_content(search_term):
    conn = db_connection()
    c = conn.cursor()

    content = c.execute("""
        SELECT content_id, title, show_type, release_year, imdb_score
        FROM Content
        WHERE title LIKE %s
        ORDER BY imdb_score
    """, (f"%{search_term}%",))
    
    content = c.fetchall()
    conn.close()
    return content