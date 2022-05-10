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
    else:
        return '<script>alert("관리자의 권한이 없습니다.");location.href="/"</script>'


@bp.route('/list/', methods=('GET', 'POST'))
@login_required
def _list():
    print("/list")
    user_list = User.query.order_by(User.id.asc())
    return render_template('admin/admin_list.html', user_list=user_list)


@bp.route('/user_delete/<int:user_id>', methods=('GET', 'POST'))
def user_delete(user_id):
    if g.user.email == "admin@naver.com":
        if user_id == 1:
            return '<script>alert("관리자 계정은 삭제가 불가능합니다.");location.href="/admin/list"</script>'
        else:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return '<script>alert("삭제되었습니다.");location.href="/admin/list"</script>'
    else:
        return '<script>alert("관리자가 아닙니다.");location.href="/"</script>'


@bp.route('/main/', methods=('GET', 'POST'))
@login_required
def main():
    return render_template('admin/admin_form.html')


@bp.route('/contact/', methods=('GET', 'POST'))
@login_required
def contact():
    print("/contact")
    contact_list = User.query.order_by(User.id.asc())
    return render_template('admin/admin_contactus.html', contact_list=contact_list)
