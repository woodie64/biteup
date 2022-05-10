from datetime import datetime
from .auth_views import login_required
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Community, Answer, User

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=('POST', 'GET'))
@login_required
def login():
    if g.user.email == "admin@naver.com":
        return '<script>alert("관리자 입니다.");location.href="/admin/main/"</script>'


@bp.route('/list/', methods=('GET', 'POST'))
@login_required
def _list():
    print("/list")
    user_list = User.query.order_by(User.id.desc())
    for user in user_list:
        print(user.email)
    return render_template('admin/admin_list.html', user_list=user_list)


@bp.route('/main/', methods=('GET', 'POST'))
@login_required
def main():
    return render_template('admin/admin_form.html')
