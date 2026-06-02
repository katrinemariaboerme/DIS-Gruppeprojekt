from flask import Flask, render_template, request, redirect, url_for
import sqlite3


def db_connection():
    conn = sqlite3.connect("watchflix.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS Content (
            content_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content_type TEXT NOT NULL,
            release_year INTEGER,
            imdb_rating REAL,
            UNIQUE(title, content_type, release_year)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS UserContentList (
            user_id INTEGER NOT NULL,
            content_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, content_id),
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (content_id) REFERENCES Content(content_id)
        )
    """)

    conn.execute("""
        INSERT OR IGNORE INTO Users (user_id, username, email, password)
        VALUES (1, 'testuser', 'test@example.com', 'password')
    """)

    sample_content = [
        ("Inception", "Movie", 2010, 8.8),
        ("Breaking Bad", "TV Show", 2008, 9.5),
        ("Interstellar", "Movie", 2014, 8.7),
        ("Stranger Things", "TV Show", 2016, 8.7),
        ("The Dark Knight", "Movie", 2008, 9.0),
        ("The Office", "TV Show", 2005, 9.0)
    ]

    for item in sample_content:
        conn.execute("""
            INSERT OR IGNORE INTO Content 
            (title, content_type, release_year, imdb_rating)
            VALUES (?, ?, ?, ?)
        """, item)

    conn.commit()
    conn.close()


init_db()

app = Flask(__name__)


@app.route("/")
def index():
    conn = db_connection()

    content = conn.execute("""
        SELECT content_id, title, content_type, release_year, imdb_rating
        FROM Content
        ORDER BY title
    """).fetchall()

    conn.close()

    return render_template("index.html", content=content)


@app.route("/watchlist")
def watchlist():
    conn = db_connection()

    items = conn.execute("""
        SELECT c.title, c.content_type, c.release_year, c.imdb_rating, ucl.status
        FROM UserContentList ucl
        JOIN Content c ON ucl.content_id = c.content_id
        WHERE ucl.user_id = 1
        AND ucl.status = 'want_to_watch'
    """).fetchall()

    conn.close()

    return render_template("watchlist.html", items=items)


@app.route("/favorites")
def favorites():
    conn = db_connection()

    favorites = conn.execute("""
        SELECT c.title, c.content_type, c.release_year, c.imdb_rating, ucl.status
        FROM UserContentList ucl
        JOIN Content c ON ucl.content_id = c.content_id
        WHERE ucl.user_id = 1
        AND ucl.status = 'favorite'
    """).fetchall()

    conn.close()

    return render_template("favorites.html", favorites=favorites)


@app.route("/add/<int:content_id>", methods=["POST"])
def add_to_watchlist(content_id):
    conn = db_connection()

    conn.execute("""
        INSERT OR IGNORE INTO UserContentList (user_id, content_id, status)
        VALUES (1, ?, 'want_to_watch')
    """, (content_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("watchlist"))


@app.route("/favorite/<int:content_id>", methods=["POST"])
def add_to_favorites(content_id):
    conn = db_connection()

    conn.execute("""
        INSERT OR IGNORE INTO UserContentList (user_id, content_id, status)
        VALUES (1, ?, 'favorite')
    """, (content_id,))

    conn.execute("""
        UPDATE UserContentList
        SET status = 'favorite'
        WHERE user_id = 1
        AND content_id = ?
    """, (content_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("favorites"))


if __name__ == "__main__":
    app.run(debug=True)