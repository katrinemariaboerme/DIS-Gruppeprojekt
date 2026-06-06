from flask import Blueprint,  render_template, request
from models.homepage import get_content_homepage

bp = Blueprint('homepage', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def homepage():
    content = get_content_homepage()
    return render_template('index.html', content=content)

