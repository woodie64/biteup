from flask import Blueprint, url_for, render_template, flash, g, session
from werkzeug.utils import redirect

from pybo.views.auth_views import login_required
from pybo import db
from pybo.forms import EditProfileForm
from pybo.models import User

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def profile():
    return render_template('profile/profile_form.html', form=form)


@bp.route('/edit/', methods=('GET', 'POST'))
@login_required
def edit():
    form = EditProfileForm()
    user = User.query.filter_by(email=g.user.email)
    if form.validate_on_submit():
        user.username = form.username.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('프로필을 수정하였습니다.')
        return redirect(url_for('auth.user', user=user))
    return render_template('profile/profile_edit.html', form=form, user=user)
