from flask import Blueprint, render_template
bp = Blueprint('index', __name__, url_prefix='/index')


@bp.route('/')
def trade():
    return render_template('index/trade.html')


@bp.route('/exchange')
def exchange():
    return render_template('index/exchange.html')
