from flask import Blueprint, url_for, render_template, flash, g, request
from werkzeug.utils import redirect
from pybo.views.auth_views import login_required

from pybo import db
from pybo.forms import EditProfileForm
from pybo.models import User

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def profile():
    return render_template('profile/profile_form.html')


@bp.route('/edit/', methods=('GET', 'POST'))
@login_required
def edit():
    print("/edit")
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            email = g.user.email
            user = User.query.filter_by(email=email).first()
            user.username = request.form['username']
            user.location = request.form['location']
            user.about_me = request.form['about_me']
            db.session.add(user)
            db.session.commit()
            alt('프로필을 수정하였습니다.')
            return redirect(url_for('profile.profile'))
        except:
            print("profile edit error")
    return render_template('profile/profile_edit.html', form=form)


@bp.route('/reset/', methods=('GET', 'POST'))
def reset():
    form = EditPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=request.args['id']).first()
        if not check_password_hash(user.password, form.password.data):
            error = '현재 비밀번호가 일치하지 않습니다'
        elif not User:
            user = generate_password_hash(form.password1.data)
            error = '새 비밀번호가 일치하지 않습니다'
        if error is None:
            db.session.add(user)
            db.session.commit()
        flash("비밀번호가 변경되었습니다.")
        return redirect(url_for('profile.profile'))
    flash(error)
    return render_template('profile/profile_reset.html', form=form)
