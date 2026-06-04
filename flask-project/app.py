from flask import Flask, render_template, request, redirect, url_for
from database import init_db
from controllers import watchlist, favorites, homepage
from models import get_content_homepage, get_watchlist, get_favorites, add_to_watchlist, add_to_favorites

init_db()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(watchlist.bp)
app.register_blueprint(favorites.bp)
app.register_blueprint(homepage.bp)