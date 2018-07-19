from flask import Blueprint, render_template

from mypack.models import Actor
from mypack.models.db import session


bp = Blueprint('web', __name__)


@bp.route('/')
def index():
    return "Index page works!"


@bp.route('/hello')
def hello():
    return render_template("web/hello.html")


@bp.route('/n_actors')
def n_actors():
    return str(session.query(Actor).count())


