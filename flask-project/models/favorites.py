from database import db_connection


def get_content_favorites(user_id):
    conn = db_connection()

    favorites = conn.execute("""
        SELECT c.content_id, c.title, c.content_type, c.release_year, c.imdb_rating, ucl.status
        FROM UserContentList ucl
        JOIN Content c ON ucl.content_id = c.content_id
        WHERE ucl.user_id = ?
        AND ucl.status = 'favorite'
        ORDER BY ucl.added_at DESC
    """, (user_id,)).fetchall()

    conn.close()
    return favorites


def add_to_favorites(content_id, user_id):
    conn = db_connection()

    conn.execute("""
        INSERT OR IGNORE INTO UserContentList (user_id, content_id, status)
        VALUES (?, ?, 'favorite')
    """, (user_id, content_id))

    conn.execute("""
        UPDATE UserContentList
        SET status = 'favorite'
        WHERE user_id = ?
        AND content_id = ?
    """, (user_id, content_id))

    conn.commit()
    conn.close()


def remove_from_favorites(content_id, user_id):
    conn = db_connection()

    conn.execute("""
        DELETE FROM UserContentList
        WHERE user_id = ?
        AND content_id = ?
        AND status = 'favorite'
    """, (user_id, content_id))

    conn.commit()
    conn.close()