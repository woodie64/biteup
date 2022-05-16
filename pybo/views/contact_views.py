from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
from datetime import datetime

from .. import db
from ..forms import ContactForm
from ..models import Contact

bp = Blueprint('contact', __name__, url_prefix='/contact')


@bp.route('/qna', methods=('GET', 'POST'))
def qna():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        contact = Contact(email=form.email.data, username=form.username.data, subject=form.subject.data, message=form.message.data,
                          create_date=datetime.today())
        db.session.add(contact)
        db.session.commit()
        return '<script>alert("작성되었습니다.");location.href="/"</script>'
    return render_template('contact/contact_form.html', form=form)
