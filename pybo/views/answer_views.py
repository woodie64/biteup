from datetime import datetime
from .auth_views import login_required
from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm
from ..models import Community, Notice, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:community_id>', methods=('POST',))
@login_required
def create(community_id):
    form = AnswerForm()
    community = Community.query.get_or_404(community_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        community.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('community.detail', community_id=community_id))
    return render_template('community/community_detail.html', community=community, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('community.detail', community_id=answer.community.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('community.detail', community_id=answer.community.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)


@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    community_id = answer.community.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('community.detail', community_id=community_id))


# notice


# @bp.route('/create/<int:notice_id>', methods=('POST',))
# @login_required
# def create(notice_id):
#     form = AnswerForm()
#     notice = Notice.query.get_or_404(notice_id)
#     if form.validate_on_submit():
#         content = request.form['content']
#         answer = Answer(content=content, create_date=datetime.now(), user=g.user)
#         notice.answer_set.append(answer)
#         db.session.commit()
#         return redirect(url_for('notice.detail', notice_id=notice_id))
#     return render_template('notice/notice_detail.html', notice=notice, form=form)
#
#
# @bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
# @login_required
# def modify(answer_id):
#     answer = Answer.query.get_or_404(answer_id)
#     if g.user != answer.user:
#         flash('수정권한이 없습니다')
#         return redirect(url_for('notice.detail', notice_id=answer.notice.id))
#     if request.method == "POST":
#         form = AnswerForm()
#         if form.validate_on_submit():
#             form.populate_obj(answer)
#             answer.modify_date = datetime.now()  # 수정일시 저장
#             db.session.commit()
#             return redirect(url_for('notice.detail', notice_id=answer.notice.id))
#     else:
#         form = AnswerForm(obj=answer)
#     return render_template('answer/answer_form.html', form=form)
#
#
# @bp.route('/delete/<int:answer_id>')
# @login_required
# def delete(answer_id):
#     answer = Answer.query.get_or_404(answer_id)
#     notice_id = answer.notice.id
#     if g.user != answer.user:
#         flash('삭제권한이 없습니다')
#     else:
#         db.session.delete(answer)
#         db.session.commit()
#     return redirect(url_for('notice.detail', notice_id=notice_id))