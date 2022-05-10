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
        return '<script>alert("관리자 입니다.");location.href="/admin/user_detail/wejrknwjernnwjrjknwwjenr"</script>'


@bp.route('/user_detail/wejrknwjernnwjrjknwwjenr', methods=('GET', 'POST'))
@login_required
def user_detail():
    print("/user_detail/wejrknwjernnwjrjknwwjenr")
    user_list = User.query.order_by(User.id.desc())
    for user in user_list:
        print(user.email)
    return render_template('admin/admin_list.html', user_list=user_list)

