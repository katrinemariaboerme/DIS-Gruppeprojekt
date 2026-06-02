from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    content = [
        (1, "Inception", "Movie", 2010, 8.8),
        (2, "Breaking Bad", "TV Show", 2008, 9.5),
        (3, "Interstellar", "Movie", 2014, 8.7),
        (4, "Stranger Things", "TV Show", 2016, 8.7)
    ]

    return render_template("index.html", content=content)


@app.route("/watchlist")
def watchlist():
    items = [
        ("Inception", "Movie", 2010, 8.8, "want_to_watch"),
        ("Breaking Bad", "TV Show", 2008, 9.5, "watched")
    ]

    return render_template("watchlist.html", items=items)


@app.route("/favorites")
def favorites():
    favorites = [
        ("Interstellar", "Movie", 2014, 8.7, "favorite"),
        ("Breaking Bad", "TV Show", 2008, 9.5, "favorite")
    ]

    return render_template("favorites.html", favorites=favorites)


@app.route("/add/<int:content_id>", methods=["POST"])
def add_to_watchlist(content_id):
    return "Add to watchlist button works"


@app.route("/favorite/<int:content_id>", methods=["POST"])
def add_to_favorites(content_id):
    return "Favorite button works"


if __name__ == "__main__":
    app.run(debug=True)