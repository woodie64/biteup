from datetime import datetime
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm, PasswordResetForm, PasswordResetConfirmForm, AgreeForm, WithdrawalForm
from pybo.models import User
import functools

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/agree', methods=('POST', 'GET'))
def agree():
    if g.user:
        session.clear()
        return '<script>alert("로그아웃 됩니다.");location.href="/agree_re"</script>'
    else:
        return '<script>location.href="/agree_re"</script>'


@bp.route('/agree_re', methods=('GET', 'POST'))
def agree_re():
    form = AgreeForm()
    if request.method == 'POST' and form.validate_on_submit():
        if not user:
            user = User(agree=form.agree.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('auth/agree_re.html', form=form)


@bp.route('/signup', methods=('POST', 'GET'))
def signup():
    if g.user:
        session.clear()
        return '<script>alert("로그아웃 됩니다.");location.href="/agree_re"</script>'
    else:
        return '<script>location.href="/signup_re"</script>'


@bp.route('/signup_re', methods=('GET', 'POST'))
def signup_re():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(email=form.email.data,
                        password=generate_password_hash(form.password1.data),
                        username=form.username.data,
                        passwd_answer=form.passwd_answer.data,
                        create_date=datetime.now())
            db.session.add(user)
            db.session.commit()
            print("계정이 생성됨")
            print(form.email.data)
            return '<script>alert("계정이 생성되었습니다.");location.href="/"</script>'
        else:
            return '<script>alert("이미 존재하는 계정입니다.");location.href="/signup_re"</script>'
    return render_template('auth/signup.html', form=form)


@bp.route('/login', methods=('POST', 'GET'))
def login():
    if g.user:
        session.clear()
        return '<script>alert("로그아웃 됩니다.");location.href="/login_re"</script>'
    else:
        return '<script>location.href="/login_re"</script>'


@bp.route('/login_re', methods=('GET', 'POST'))
def login_re():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = '올바른 이메일 주소를 입력하세요'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 일치하지 않습니다'
        if error is None:
            print("로그인 : "+user.email)
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index._list'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout')
def logout():
    print("로그아웃 : " + g.user.email)
    session.clear()
    return redirect(url_for('index._list'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/password_reset', methods=('GET', 'POST'))
def password_reset():
    form = PasswordResetForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data,
                                    username=form.username.data,
                                    passwd_answer=form.passwd_answer.data).first()
        if not user:
            print("등록되지 않은 사용자 비밀번호 변경")
            return '<script>alert("등록되지 않은 사용자 정보입니다.");location.href="/password_reset"</script>'
        if error is None:
            return redirect(url_for('auth.password_reset_confirm', id=form.email.data))
    return render_template('auth/password_reset.html', form=form)


@bp.route('/password_reset_confirm', methods=('GET', 'POST'))
def password_reset_confirm():
    form = PasswordResetConfirmForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=request.args['id']).first()
        user.password = generate_password_hash(form.password1.data)
        db.session.add(user)
        db.session.commit()
        print(user.email)
        print("비밀번호 변경됨")
        return '<script>alert("비밀번호가 변경되었습니다.");location.href="/login"</script>'
    return render_template('auth/password_reset_confirm.html', form=form)


@bp.route('/delete_user', methods=('GET', 'POST'))
@login_required
def delete_user():
    form = WithdrawalForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        if not check_password_hash(g.user.password, form.password.data):
            error = '<script>alert("비밀번호가 일치하지 않습니다.");location.href="/delete_user"</script>'
        if error is None:
            user = User.query.get(g.user.id)
            db.session.delete(user)
            db.session.commit()
            print("계정 탈퇴함")
            return '<script>alert("탈퇴되었습니다.");location.href="/"</script>'
    return render_template('auth/withdrawal.html', form=form)


@bp.route('/paper/provision')
def provision():
    return render_template('auth/provision.html')


@bp.route('/paper/privacy')
def privacy():
    return render_template('auth/privacy.html')
