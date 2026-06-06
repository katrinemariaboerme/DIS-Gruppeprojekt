from database import db_connection


def get_content_watchlist():
    conn = db_connection()
    c = conn.cursor()

    watchlist = c.execute("""
        SELECT c.content_id, c.title, c.show_type, c.release_year, c.imdb_score, ucl.status
        FROM Watchlist ucl
        JOIN Content c ON ucl.content_id = c.content_id
        WHERE ucl.status = 'want_to_watch'
        ORDER BY ucl.added_at DESC
    """)
    watchlist = c.fetchall()

    conn.close()
    return watchlist


def add_to_watchlist(content_id):
    conn = db_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO Watchlist (content_id, status)
        VALUES (%s, 'want_to_watch')
        ON CONFLICT DO NOTHING
    """, (content_id,))

    conn.commit()
    conn.close()


def remove_from_watchlist(content_id):
    conn = db_connection()
    c = conn.cursor()

    c.execute("""
        DELETE FROM Watchlist
        WHERE content_id = %s
        AND status = 'want_to_watch'
    """, (content_id))

    conn.commit()
    conn.close()