from database import db_connection


def get_content_homepage():
    conn = db_connection()

    content = conn.execute("""
        SELECT content_id, title, content_type, release_year, imdb_rating
        FROM Content
        ORDER BY title
    """).fetchall()

    conn.close()
    return content


def search_content(search_term):
    conn = db_connection()

    content = conn.execute("""
        SELECT content_id, title, content_type, release_year, imdb_rating
        FROM Content
        WHERE title LIKE ?
        ORDER BY title
    """, (f"%{search_term}%",)).fetchall()

    conn.close()
    return content