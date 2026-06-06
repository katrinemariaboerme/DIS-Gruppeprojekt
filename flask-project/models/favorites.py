from database import db_connection


def get_content_favorites():
    conn = db_connection()
    c = conn.cursor()

    favorites = c.execute("""
        SELECT c.content_id, c.title, c.show_type, c.release_year, c.imdb_score, ucl.status
        FROM Favourites ucl
        JOIN Content c ON ucl.content_id = c.content_id
        WHERE ucl.status = 'favorite'
        ORDER BY ucl.added_at DESC
    """)
    favorites = c.fetchall()

    conn.close()
    return favorites


def add_to_favorites(content_id):
    conn = db_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO Favourites (content_id, status)
        VALUES (%s, 'favorite')
        ON CONFLICT DO NOTHING
    """, (content_id,))
    conn.commit()
    conn.close()


def remove_from_favorites(content_id):
    conn = db_connection()
    c = conn.cursor()

    c.execute("""
        DELETE FROM Favourites
        WHERE content_id = %s
        AND status = 'favorite'
    """, (content_id,))

    conn.commit()
    conn.close()