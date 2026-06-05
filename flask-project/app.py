from flask import Flask
from database import init_db
from controllers import watchlist, favorites, homepage

init_db()

app = Flask(__name__)

app.register_blueprint(homepage.bp)
app.register_blueprint(watchlist.bp)
app.register_blueprint(favorites.bp)

if __name__ == "__main__":
    app.run(debug=True)

    