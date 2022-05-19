from flask import Blueprint, render_template, request, url_for, g, flash, send_file
from werkzeug.utils import secure_filename

from .. import db
from ..forms import CommunityForm, AnswerForm
from ..models import Community, Answer, User

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def trade():
    return render_template('index/trade.html')


@bp.route('/')
def _list():
    community_list = Community.query.order_by(Community.create_date.desc())
    return render_template('index/trade.html', community_list=community_list)


@bp.route('/exchange')
def exchange():
    return render_template('index/exchange.html')


@bp.route('/testpage')
def testpage():
    return render_template('index/testpage.html')