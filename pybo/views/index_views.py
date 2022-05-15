from flask import Blueprint, render_template
bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/')
def trade():
    return render_template('index/trade.html')


@bp.route('/')
def _list():
    community_list = Community.query.order_by(Community.create_date.desc())
    community_list = community_list.paginate(page, per_page=10)
    return render_template('index/trade.html', community_list=community_list, page=page)


@bp.route('/exchange')
def exchange():
    return render_template('index/exchange.html')
