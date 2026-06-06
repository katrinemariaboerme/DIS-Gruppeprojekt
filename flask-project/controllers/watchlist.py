from flask import Blueprint,  render_template, request, redirect
from database import db_connection
from models.watchlist import get_content_watchlist, add_to_watchlist

bp = Blueprint('watchlist', __name__, url_prefix='/')

@bp.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    if request.method == 'POST':
        content_id = request.form['content_id']
        if content_id:
            add_to_watchlist(content_id)
        return redirect('/watchlist')
    watchlist_content = get_content_watchlist()    

    return render_template('watchlist.html', watchlist=watchlist_content)