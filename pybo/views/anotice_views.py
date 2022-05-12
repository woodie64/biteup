from datetime import datetime
from .auth_views import login_required
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import AnoticeForm
from ..models import Anotice, Notice

bp = Blueprint('anotice', __name__, url_prefix='/anotice')


@bp.route('/create/<int:notice_id>', methods=('POST',))
@login_required
def create(notice_id):
    form = AnoticeForm()
    notice = Notice.query.get_or_404(notice_id)
    if form.validate_on_submit():
        content = request.form['content']
        anotice = Anotice(content=content, create_date=datetime.now(), user=g.user)
        notice.anotice_set.append(anotice)
        db.session.commit()
        return redirect(url_for('notice.detail', notice_id=notice_id))
    return render_template('notice/notice_detail.html', notice=notice, form=form)


@bp.route('/modify/<int:anotice_id>', methods=('GET', 'POST'))
@login_required
def modify(anotice_id):
    anotice = Anotice.query.get_or_404(anotice_id)
    form = AnoticeForm(obj=anotice)
    if g.user != anotice.user:
        # flash('수정권한이 없습니다')
        return '<script>alert("수정권한이 없습니다");location.href="/anotice/detail/' + str(anotice.notice.id) + '"</script>'
        # return redirect(url_for('notice.detail', notice_id=anotice.notice.id))
    if request.method == "POST":
        form = AnoticeForm()
        if form.validate_on_submit():
            form.populate_obj(anotice)
            anotice.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return '<script>alert("수정되었습니다.");location.href="/notice/detail/' + str(anotice.notice.id) + '"</script>'
            # return redirect(url_for('notice.detail', notice_id=anotice.notice.id))

    return render_template('anotice/anotice_form.html', form=form)


@bp.route('/delete/<int:anotice_id>')
@login_required
def delete(anotice_id):
    anotice = Anotice.query.get_or_404(anotice_id)
    notice_id = anotice.notice.id
    if g.user != anotice.user:
        # flash('삭제권한이 없습니다')
        return '<script>alert("삭제권한이 없습니다");location.href="/notice/detail/'+str(notice_id)+'"</script>'
    else:
        db.session.delete(answer)
        db.session.commit()
        return '<script>alert("삭제되었습니다.");location.href="/notice/detail/'+str(notice_id) + '"</script>'
    return redirect(url_for('notice.detail', notice_id=notice_id))

