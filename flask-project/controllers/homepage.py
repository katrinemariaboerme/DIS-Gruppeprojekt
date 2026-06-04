from flask import Blueprint,  render_template, request
from database import db_connection
from models.homepage import get_content_homepage

bp = Blueprint('homepage', __name__, url_prefix='/')

@bp.route('/homepage', methods=['GET'])
def homepage():
    content = get_content_homepage()
    return render_template('homepage.html', content=content)

