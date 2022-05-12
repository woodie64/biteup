from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect

from .. import db
from ..forms import ContactForm
from ..models import Contact

bp = Blueprint('contact', __name__, url_prefix='/contact')


@bp.route('/qna/', methods=('GET', 'POST'))
def qna():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        contact = Contact(email=form.email.data, username=form.username.data, subject=form.subject.data, message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('index.trade'))
    return render_template('contact/contact_form.html', form=form)
