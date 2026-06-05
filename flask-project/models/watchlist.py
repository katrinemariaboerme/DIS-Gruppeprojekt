from database import db_connection


def get_content_watchlist(user_id):
    conn = db_connection()

    watchlist = conn.execute("""
        SELECT c.content_id, c.title, c.content_type, c.release_year, c.imdb_rating, ucl.status
        FROM UserContentList ucl
        JOIN Content c ON ucl.content_id = c.content_id
        WHERE ucl.user_id = ?
        AND ucl.status = 'want_to_watch'
        ORDER BY ucl.added_at DESC
    """, (user_id,)).fetchall()

    conn.close()
    return watchlist


def add_to_watchlist(content_id, user_id):
    conn = db_connection()

    conn.execute("""
        INSERT OR IGNORE INTO UserContentList (user_id, content_id, status)
        VALUES (?, ?, 'want_to_watch')
    """, (user_id, content_id))

    conn.commit()
    conn.close()


def remove_from_watchlist(content_id, user_id):
    conn = db_connection()

    conn.execute("""
        DELETE FROM UserContentList
        WHERE user_id = ?
        AND content_id = ?
        AND status = 'want_to_watch'
    """, (user_id, content_id))

    conn.commit()
    conn.close()