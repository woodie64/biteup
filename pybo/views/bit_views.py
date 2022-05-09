from flask import Blueprint, render_template, request, url_for, g, flash
from ..models import Community, Answer, User
bp = Blueprint('index', __name__, url_prefix='/index')


@bp.route('/')
def trade():
    return render_template('index/trade.html')

