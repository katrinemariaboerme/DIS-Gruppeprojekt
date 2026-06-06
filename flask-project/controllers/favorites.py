from flask import Blueprint,  render_template, request, redirect
from database import db_connection
from models.favorites import get_content_favorites, add_to_favorites, remove_from_favorites

bp = Blueprint('favorites', __name__, url_prefix='/')

@bp.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'POST':
        content_id = request.form['content_id']
        if content_id :
            add_to_favorites(content_id)
        return redirect('/favorites')
    favorites_content = get_content_favorites()    

    return render_template('favorites.html', favorites=favorites_content)