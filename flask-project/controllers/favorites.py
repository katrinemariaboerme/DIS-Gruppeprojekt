from flask import Blueprint,  render_template, request
from models.favorites import add_to_favorites, get_content_favorites
from database import db_connection

bp = Blueprint('favorites', __name__, url_prefix='/')

@bp.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'POST':
        content_id = request.form['content_id']
        add_to_favorites(content_id) # and user id?

    return render_template('favorites.html', favorites=get_content_favorites())