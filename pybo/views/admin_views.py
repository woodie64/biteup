from datetime import datetime
from .auth_views import login_required
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Community, Answer, User, Contact

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=('POST', 'GET'))
@login_required
def login():
    if g.user.email == "biteup@biteup.com":
        print("관리자 페이지 접근 성공: " + g.user.email)
        return '<script>alert("관리자 입니다.");location.href="/admin/main"</script>'
    else:
        print("관리자 페이지 접근 실패 : " + g.user.email)
        return '<script>alert("관리자가 아닙니다.");location.href="/"</script>'


@bp.route('/list', methods=('GET', 'POST'))
@login_required
def _list():
    if g.user.email == "biteup@biteup.com":
        user_list = User.query.order_by(User.id.asc())
        return render_template('admin/admin_list.html', user_list=user_list)
    else:
        return '<script>alert("관리자의 권한이 없습니다.");location.href="/"</script>'


@bp.route('/user_delete<int:user_id>', methods=('GET', 'POST'))
def user_delete(user_id):
    if g.user.email == "biteup@biteup.com":
        if user_id == 1:
            return '<script>alert("관리자 계정은 삭제가 불가능합니다.");location.href="/admin/list"</script>'
        else:
            user = User.query.get_or_404(user_id)
            #로깅
            print("관리자 페이지 : 계정 삭제")
            print(g.user.email+" -> "+user.email)
            ###
            db.session.delete(user)
            db.session.commit()
            return '<script>alert("삭제되었습니다.");location.href="/admin/list"</script>'
    else:
        return '<script>alert("관리자의 권한이 없습니다.");location.href="/"</script>'


@bp.route('/main', methods=('GET', 'POST'))
@login_required
def main():
    if g.user.email == "biteup@biteup.com":
        print("/admin/main에 접근 시도 : " + g.user.email)
        return render_template('admin/admin_form.html')
    else:
        return '<script>alert("관리자의 권한이 없습니다.");location.href="/"</script>'


@bp.route('/contact', methods=('GET', 'POST'))
@login_required
def contact():
    if g.user.email == "biteup@biteup.com":
        contact_list = Contact.query.order_by(Contact.id.desc())
        return render_template('admin/admin_contactus.html', contact_list=contact_list)
    else:
        return '<script>alert("관리자의 권한이 없습니다.");location.href="/"</script>'


@bp.route('/contact_delete<int:contact_id>', methods=('GET', 'POST'))
def contact_delete(contact_id):
    if g.user.email == "biteup@biteup.com":
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return '<script>alert("삭제되었습니다.");location.href="/admin/contact"</script>'
    else:
        return '<script>alert("관리자의 권한이 없습니다.");location.href="/"</script>'
