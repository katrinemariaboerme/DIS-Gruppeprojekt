from flask import Blueprint,  render_template, redirect
from models.favorites import get_content_favorites, add_to_favorites

bp = Blueprint('favorites', __name__, url_prefix='/')

@bp.route('/favorites', methods=['GET'])
def favorites():
    favorites_content = get_content_favorites()
    return render_template('favorites.html',favorites=favorites_content)

@bp.route('/favorite/<content_id>', methods=['POST'])
def add(content_id):
    add_to_favorites(content_id)
    return redirect('/')