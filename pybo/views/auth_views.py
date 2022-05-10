from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from django.core.mail.message import EmailMessage

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm, PasswordResetForm, PasswordResetConfirmForm, AgreeForm
from pybo.models import User
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/agree/', methods=('GET', 'POST'))
def agree_re():
    form = AgreeForm()
    if request.method == 'POST' and form.validate_on_submit():
        if not user:
            user = User(agree=form.agree.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('auth/agree_re.html', form=form)


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(email=form.email.data,
                        password=generate_password_hash(form.password1.data),
                        username=form.username.data,
                        passwd_answer=form.passwd_answer.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = '올바른 이메일 주소를 입력하세요'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 일치하지 않습니다'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/password_reset/', methods=('GET', 'POST'))
def password_reset():
    form = PasswordResetForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data,
                                    username=form.username.data,
                                    passwd_answer=form.passwd_answer.data).first()
        if not user:
            error = '등록되지 않은 사용자 정보입니다.'
            flash(error)
        if error is None:
            return redirect(url_for('auth.password_reset_confirm', id=form.email.data))
    return render_template('auth/password_reset.html', form=form)


@bp.route('/password_reset_confirm/', methods=('GET', 'POST'))
def password_reset_confirm():
    form = PasswordResetConfirmForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=request.args['id']).first()
        user.password = generate_password_hash(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash("비밀번호가 변경되었습니다.")
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset_confirm.html', form=form)
