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
    form = EditProfileForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data,
                                    location=form.location.data,
                                    about_me=form.about_me.data)
        db.session.add(user)
        db.session.commit()
        flash('프로필을 수정하였습니다.')
        return redirect(url_for('profile.profile'))
    return render_template('profile/profile_edit.html', form=form)
