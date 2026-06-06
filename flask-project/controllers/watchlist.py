from flask import Blueprint,  render_template, redirect
from models.watchlist import get_content_watchlist, add_to_watchlist

bp = Blueprint('watchlist', __name__, url_prefix='/')

@bp.route('/watchlist', methods=['GET'])
def watchlist():
    watchlist_content = get_content_watchlist()
    return render_template('watchlist.html',watchlist=watchlist_content)

@bp.route('/add/<content_id>', methods=['POST'])
def add(content_id):
    add_to_watchlist(content_id)
    return redirect('/')
