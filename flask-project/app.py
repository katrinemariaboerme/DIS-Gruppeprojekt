from flask import Flask
from controllers import watchlist, favorites, homepage

app = Flask(__name__)

app.register_blueprint(homepage.bp)
app.register_blueprint(watchlist.bp)
app.register_blueprint(favorites.bp)

if __name__ == "__main__":
    app.run(debug=True)

    